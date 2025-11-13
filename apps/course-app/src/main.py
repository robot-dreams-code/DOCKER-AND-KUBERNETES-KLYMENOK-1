import os
import socket
import time
import math
import threading
import sqlite3
from datetime import datetime
from typing import List, Dict, Any, Optional

from fastapi import FastAPI, HTTPException, Form, Query, Request
from fastapi.responses import HTMLResponse, JSONResponse

try:
    import redis  # type: ignore
except Exception:  # pragma: no cover - optional dependency for sqlite-only use
    redis = None
try:
    import httpx  # type: ignore
except Exception:  # pragma: no cover - optional dependency for non-http use
    httpx = None
import uuid
import contextvars


APP_MESSAGE = os.getenv("APP_MESSAGE", "Welcome to the Course App")
SECRET_TOKEN = os.getenv("APP_SECRET_TOKEN", "")
STORE_BACKEND = os.getenv("APP_STORE", "sqlite").lower()
DB_PATH = os.getenv("APP_DB_PATH", "data/data.sql")
REDIS_URL = os.getenv("APP_REDIS_URL", "redis://localhost:6379/0")
MESSAGES_API = os.getenv("APP_MESSAGES_API", "").rstrip("/")
COUNTER_API = os.getenv("APP_COUNTER_API", "").rstrip("/")
HOSTNAME = socket.gethostname()
REQ_ID_CTX: contextvars.ContextVar[str] = contextvars.ContextVar("req_id", default="")


class Store:
    name = "base"

    def init(self) -> None:
        raise NotImplementedError

    def ping(self) -> None:
        raise NotImplementedError

    def get_counter(self, name: str) -> int:
        raise NotImplementedError

    def incr_counter(self, name: str, delta: int = 1) -> int:
        raise NotImplementedError

    def add_message(self, text: str) -> None:
        raise NotImplementedError

    def list_messages(self, limit: int = 20) -> List[Dict[str, Any]]:
        raise NotImplementedError


class SqliteStore(Store):
    name = "sqlite"

    def __init__(self, path: str) -> None:
        self.path = path

    def init(self) -> None:
        dirpath = os.path.dirname(self.path) or "."
        os.makedirs(dirpath, exist_ok=True)
        conn = sqlite3.connect(self.path)
        try:
            cur = conn.cursor()
            cur.execute(
                "CREATE TABLE IF NOT EXISTS counters (key TEXT PRIMARY KEY, value INTEGER)"
            )
            cur.execute(
                "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT NOT NULL, created_at TEXT NOT NULL)"
            )
            cur.execute("INSERT OR IGNORE INTO counters(key, value) VALUES('visits', 0)")
            conn.commit()
        finally:
            conn.close()

    def ping(self) -> None:
        conn = sqlite3.connect(self.path)
        try:
            cur = conn.cursor()
            cur.execute("SELECT 1")
            cur.fetchone()
        finally:
            conn.close()

    def get_counter(self, name: str) -> int:
        conn = sqlite3.connect(self.path)
        try:
            cur = conn.cursor()
            cur.execute("SELECT value FROM counters WHERE key=?", (name,))
            row = cur.fetchone()
            return int(row[0]) if row else 0
        finally:
            conn.close()

    def incr_counter(self, name: str, delta: int = 1) -> int:
        conn = sqlite3.connect(self.path)
        try:
            cur = conn.cursor()
            cur.execute("UPDATE counters SET value = value + ? WHERE key=?", (delta, name))
            if cur.rowcount == 0:
                cur.execute("INSERT INTO counters(key, value) VALUES(?, ?)", (name, delta))
            conn.commit()
            cur.execute("SELECT value FROM counters WHERE key=?", (name,))
            return int(cur.fetchone()[0])
        finally:
            conn.close()

    def add_message(self, text: str) -> None:
        conn = sqlite3.connect(self.path)
        try:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO messages(text, created_at) VALUES(?, ?)", (text, datetime.utcnow().isoformat())
            )
            conn.commit()
        finally:
            conn.close()

    def list_messages(self, limit: int = 20) -> List[Dict[str, Any]]:
        conn = sqlite3.connect(self.path)
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT id, text, created_at FROM messages ORDER BY id DESC LIMIT ?",
                (limit,),
            )
            rows = cur.fetchall()
            return [{"id": r[0], "text": r[1], "created_at": r[2]} for r in rows]
        finally:
            conn.close()


class RedisStore(Store):
    name = "redis"

    def __init__(self, url: str) -> None:
        if redis is None:
            raise RuntimeError("redis package not installed")
        # decode_responses=True to work with strings
        self.client = redis.Redis.from_url(url, decode_responses=True)

    def init(self) -> None:
        # nothing to initialize schema-wise
        # ensure 'visits' counter exists
        self.client.setnx("counters:visits", 0)

    def ping(self) -> None:
        self.client.ping()

    def get_counter(self, name: str) -> int:
        v = self.client.get(f"counters:{name}")
        return int(v) if v is not None else 0

    def incr_counter(self, name: str, delta: int = 1) -> int:
        return int(self.client.incrby(f"counters:{name}", delta))

    def add_message(self, text: str) -> None:
        msg_id = int(self.client.incr("messages:seq"))
        key = f"message:{msg_id}"
        self.client.hset(
            key,
            mapping={
                "id": msg_id,
                "text": text,
                "created_at": datetime.utcnow().isoformat(),
            },
        )
        # newest first for quick pagination
        self.client.lpush("messages:ids", msg_id)

    def list_messages(self, limit: int = 20) -> List[Dict[str, Any]]:
        ids = self.client.lrange("messages:ids", 0, max(0, limit - 1))
        items: List[Dict[str, Any]] = []
        for s in ids:
            msg_id = int(s)
            data = self.client.hgetall(f"message:{msg_id}")
            if data:
                # ensure correct types/shape
                items.append(
                    {
                        "id": int(data.get("id", msg_id)),
                        "text": data.get("text", ""),
                        "created_at": data.get("created_at", ""),
                    }
                )
        return items


class HttpStore(Store):
    name = "http"

    def __init__(self, messages_api: Optional[str], counter_api: Optional[str]):
        if httpx is None:
            raise RuntimeError("httpx package not installed")
        self.messages_api = messages_api  # like http://messages.course-app.svc.cluster.local/api
        self.counter_api = counter_api    # like http://counter.course-app.svc.cluster.local/api
        self.base_headers = {"X-App-Pod": HOSTNAME}

    def _headers(self) -> Dict[str, str]:
        h = dict(self.base_headers)
        rid = REQ_ID_CTX.get()
        if rid:
            h["X-Request-ID"] = rid
        return h

    def init(self) -> None:
        # nothing to init
        pass

    def ping(self) -> None:
        # any call to validate availability; prefer counter if set, else messages
        url = None
        if self.counter_api:
            url = f"{self.counter_api}/counter/visits"
        elif self.messages_api:
            url = f"{self.messages_api}/messages?limit=1"
        if url:
            with httpx.Client(timeout=2.0, headers=self._headers()) as c:
                r = c.get(url)
                r.raise_for_status()

    def get_counter(self, name: str) -> int:
        if not self.counter_api:
            # best effort fallback: keep a local zero
            return 0
        with httpx.Client(timeout=3.0, headers=self._headers()) as c:
            r = c.get(f"{self.counter_api}/counter/{name}")
            r.raise_for_status()
            data = r.json()
            return int(data.get("value", 0))

    def incr_counter(self, name: str, delta: int = 1) -> int:
        if not self.counter_api:
            return 0
        with httpx.Client(timeout=3.0, headers=self._headers()) as c:
            r = c.post(f"{self.counter_api}/counter/{name}/incr", params={"delta": delta})
            r.raise_for_status()
            data = r.json()
            return int(data.get("value", 0))

    def add_message(self, text: str) -> None:
        if not self.messages_api:
            return
        with httpx.Client(timeout=3.0, headers=self._headers()) as c:
            r = c.post(f"{self.messages_api}/messages", data={"text": text})
            r.raise_for_status()

    def list_messages(self, limit: int = 20) -> List[Dict[str, Any]]:
        if not self.messages_api:
            return []
        with httpx.Client(timeout=3.0, headers=self._headers()) as c:
            r = c.get(f"{self.messages_api}/messages", params={"limit": limit})
            r.raise_for_status()
            data = r.json()
            items = data.get("items", [])
            # ensure shape
            out: List[Dict[str, Any]] = []
            for it in items:
                out.append({
                    "id": int(it.get("id", 0)),
                    "text": str(it.get("text", "")),
                    "created_at": str(it.get("created_at", "")),
                })
            return out


def create_store() -> Store:
    # http microservices mode (messages + counter services)
    if STORE_BACKEND == "http" or (MESSAGES_API or COUNTER_API):
        return HttpStore(messages_api=MESSAGES_API or None, counter_api=COUNTER_API or None)
    if STORE_BACKEND == "redis":
        return RedisStore(REDIS_URL)
    # default to sqlite
    return SqliteStore(DB_PATH)


app = FastAPI(title="Course App")
store: Store = create_store()

@app.middleware("http")
async def add_request_id(request: Request, call_next):
    req_id = request.headers.get("x-request-id") or uuid.uuid4().hex[:12]
    REQ_ID_CTX.set(req_id)
    response = await call_next(request)
    response.headers["X-Request-ID"] = req_id
    return response


@app.on_event("startup")
def on_startup():
    store.init()


@app.get("/", response_class=HTMLResponse)
def index():
    visits = store.incr_counter("visits", 1)
    hostname = socket.gethostname()
    html = f"""
        <html>
            <head>
                <title>Course App</title>
                <meta name=viewport content="width=device-width, initial-scale=1" />
                <link rel="preconnect" href="https://fonts.googleapis.com" />
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
                <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet" />
                <style>
                    :root {{
                        --bg:#0b1020;
                        --bg-grad1:#0b1020; /* start */
                        --bg-grad2:#0d1330; /* mid */
                        --bg-grad3:#0a0f28; /* end */
                        --card:#101833cc; /* translucent */
                        --card-border:#28345f80;
                        --text:#e6e8ef;
                        --muted:#a7b0c0;
                        --accent:#7aa2f7;
                        --accent-600:#5d87f6;
                        --accent-700:#4b75ea;
                        --ok:#98c379; --warn:#e5c07b; --err:#e06c75;
                        --ring:#9ab6ff;
                    }}

                    * {{ box-sizing: border-box; }}
                    html, body {{ height: 100%; }}
                    body {{
                        font-family: "Inter", system-ui, -apple-system, Segoe UI, Roboto, sans-serif;
                        margin:0;
                        color:var(--text);
                        background:
                            radial-gradient(1200px 600px at 10% -10%, #20327544, transparent 60%),
                            radial-gradient(1000px 500px at 95% 10%, #1b254d55, transparent 60%),
                            linear-gradient(180deg, var(--bg-grad1) 0%, var(--bg-grad2) 40%, var(--bg-grad3) 100%);
                    }}

                    .wrap {{
                        max-width: 1100px;
                        margin: 0 auto;
                        padding: 32px clamp(20px, 4vw, 40px) 48px;
                    }}

                    header.app {{
                        display:flex; align-items:flex-start; justify-content:space-between; gap:16px;
                        margin-bottom: 24px;
                    }}
                    h1 {{ margin: 0; font-size: clamp(28px, 2.4vw, 36px); letter-spacing: -0.015em; }}
                    p.lead {{ margin: 8px 0 0 0; color: var(--muted); font-size: 15px; }}

                    .pillbar {{ margin:12px 0 24px 0; display:flex; flex-wrap:wrap; gap:10px; }}
                    .badge {{
                        display:inline-flex; align-items:center; gap:6px;
                        background: #1b254dcc; color:#dde6ff; padding:7px 12px;
                        border:1px solid #2a376ecc; border-radius:999px; font-size:13px;
                        backdrop-filter: blur(6px);
                    }}

                    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }}
                    .card {{
                        background: var(--card);
                        border:1px solid var(--card-border);
                        border-radius: 16px;
                        padding: 22px;
                        box-shadow: 0 8px 32px rgba(0,0,0,0.35);
                        backdrop-filter: blur(10px);
                    }}
                    .card h3 {{ margin: 0 0 16px 0; font-size: 18px; font-weight: 600; }}

                    label {{ display:block; font-size: 13px; font-weight: 500; color: var(--muted); margin-bottom: 8px; }}
                    input[type=text], input[type=number] {{
                        width:100%; background:#0f1736; color:var(--text); font-size: 14px;
                        border:1px solid #2b3970; padding:11px 14px; border-radius:10px;
                        outline: none; transition: box-shadow .15s ease, border-color .15s ease;
                    }}
                    input[type=text]:focus, input[type=number]:focus {{
                        border-color: var(--ring);
                        box-shadow: 0 0 0 3px #9ab6ff33;
                    }}

                    button {{
                        background: linear-gradient(180deg, var(--accent) 0%, var(--accent-600) 90%);
                        border: 1px solid #4569d6;
                        color: #0b1020; font-weight: 700; font-size: 14px; letter-spacing: .01em;
                        padding: 11px 16px; border-radius: 10px; cursor: pointer;
                        transition: transform .06s ease, filter .2s ease, box-shadow .2s ease;
                        box-shadow: 0 6px 18px #2540a855;
                    }}
                    button:hover {{ filter: brightness(1.02); box-shadow: 0 8px 22px #2540a866; }}
                    button:active {{ transform: translateY(1px); }}
                    button:disabled {{ opacity: .6; cursor: default; box-shadow:none; }}

                    ul.msgs {{
                        list-style:none; padding:0; margin:0;
                        display:flex; flex-direction:column; gap:12px;
                        max-height:300px; overflow-y:auto;
                        scrollbar-width: thin;
                        scrollbar-color: #2b3970 transparent;
                    }}
                    ul.msgs::-webkit-scrollbar {{ width: 8px; }}
                    ul.msgs::-webkit-scrollbar-track {{ background: transparent; }}
                    ul.msgs::-webkit-scrollbar-thumb {{ background: #2b3970; border-radius: 4px; }}
                    ul.msgs::-webkit-scrollbar-thumb:hover {{ background: #3a4a8a; }}
                    ul.msgs li {{ background:#0f1632; border:1px solid #2b3970; padding:14px; border-radius:10px; }}

                    .row {{ display:flex; gap:12px; align-items:center; flex-wrap:wrap; }}
                    code {{ background:#0f1632; border:1px solid #2b3970; padding:4px 9px; border-radius:8px; font-size: 13px; }}
                    a {{ color:#9ab6ff; text-decoration: none; }}
                    a:hover {{ text-decoration: underline; }}
                </style>
            </head>
      <body>
                <div class="wrap">
                    <header class="app">
                        <div>
                            <h1>Docker & Kubernetes Course App</h1>
                            <p class="lead">{APP_MESSAGE}</p>
                        </div>
                    </header>
                    <div class="pillbar">
                        <span class="badge">pod: {hostname}</span>
                        <span class="badge">store: {store.name}</span>
                        <span class="badge">visits: <span id="visits">{visits}</span></span>
                    </div>

          <div class="grid">
            <section class="card">
              <h3>Messages</h3>
              <form id="msgForm" onsubmit="return false;" style="margin-bottom:14px">
                <label for="msgInput">Post a message</label>
                <div class="row">
                  <input id="msgInput" type="text" placeholder="Type a message..." />
                  <button id="btnPost">Send</button>
                </div>
                <div id="msgStatus" style="font-size:13px;color:var(--muted);margin-top:6px;"></div>
              </form>
              <ul id="msgList" class="msgs"></ul>
            </section>

            <section class="card">
              <h3>Stress CPU</h3>
              <label for="secInput">Duration (seconds)</label>
              <div class="row" style="margin-bottom:12px">
                <input id="secInput" type="number" min="1" max="120" value="10" style="max-width:140px" />
                <button id="btnStress">Start</button>
              </div>
              <div id="stressStatus" style="font-size:13px;color:var(--muted);margin-bottom:14px;">Runs background CPU work to demo HPA.</div>
              <div style="margin-bottom:14px">
                <div class="row" style="gap:8px">
                  <button id="btnHealth">Check /healthz</button>
                  <button id="btnReady">Check /readyz</button>
                </div>
                <div id="hzStatus" style="font-size:13px;margin-top:10px;color:var(--muted);"></div>
              </div>
              <div style="font-size:13px;color:var(--muted);line-height:1.5;">
                Try API: <code>/healthz</code>, <code>/readyz</code>, <code>/api/info</code>, <code>/api/messages</code>, <code>/stress?seconds=10</code>
              </div>
            </section>
          </div>
        </div>

        <script>
          async function fetchJSON(url, opts={{}}) {{
            const r = await fetch(url, opts);
            if (!r.ok) throw new Error(await r.text());
            return r.json();
          }}

          async function loadMessages() {{
            try {{
              const data = await fetchJSON('/api/messages?limit=50');
              const list = document.getElementById('msgList');
              list.innerHTML = '';
              for (const it of (data.items || [])) {{
                const li = document.createElement('li');
                const dt = new Date(it.created_at || '').toLocaleString();
                li.innerHTML = `<div style="font-size:12px;color:var(--muted)">#${{it.id}} • ${{dt}}</div><div>${{(it.text||'')}}</div>`;
                list.appendChild(li);
              }}
            }} catch(e) {{
              console.warn('loadMessages failed', e);
            }}
          }}

          async function refreshVisits() {{
            try {{
              const data = await fetchJSON('/api/counter/visits');
              document.getElementById('visits').textContent = data.value;
            }} catch {{ /* ignore */ }}
          }}

          document.getElementById('btnPost').addEventListener('click', async () => {{
            const input = document.getElementById('msgInput');
            const btn = document.getElementById('btnPost');
            const st = document.getElementById('msgStatus');
            const text = (input.value || '').trim();
            if (!text) return;
            btn.disabled = true; st.textContent = 'Posting...';
            try {{
              const body = new URLSearchParams(); body.set('text', text);
              await fetchJSON('/api/messages', {{ method:'POST', headers:{{'Content-Type':'application/x-www-form-urlencoded'}}, body }});
              input.value=''; st.textContent = 'Posted!';
              await loadMessages(); await refreshVisits();
            }} catch(e) {{
              st.textContent = 'Error: ' + (e.message || 'failed');
            }} finally {{ btn.disabled = false; }}
          }});

          document.getElementById('btnStress').addEventListener('click', async () => {{
            const sec = Math.max(1, Math.min(120, parseInt(document.getElementById('secInput').value || '10')));
            const st = document.getElementById('stressStatus');
            st.textContent = 'Starting stress for ' + sec + 's...';
            try {{
              await fetchJSON(`/stress?seconds=${{sec}}&background=true`);
              st.textContent = 'Stress started. Generate load in parallel to see HPA.';
            }} catch(e) {{ st.textContent = 'Error: ' + (e.message || 'failed'); }}
          }});

          document.getElementById('btnHealth').addEventListener('click', async () => {{
            const st = document.getElementById('hzStatus');
            try {{ const x = await fetchJSON('/healthz'); st.textContent = 'Health: ' + x.status; }}
            catch(e) {{ st.textContent = 'Health error'; }}
          }});
          document.getElementById('btnReady').addEventListener('click', async () => {{
            const st = document.getElementById('hzStatus');
            try {{ const x = await fetchJSON('/readyz'); st.textContent = 'Ready: ' + x.status; }}
            catch(e) {{ st.textContent = 'Ready error'; }}
          }});

          loadMessages();
        </script>
      </body>
    </html>
    """
    return HTMLResponse(content=html)


@app.get("/api/counter/{name}")
def api_counter(name: str):
    try:
        val = store.get_counter(name)
        return {"name": name, "value": val}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/healthz")
def healthz():
    return {"status": "ok"}


@app.get("/readyz")
def readyz():
    try:
        # check store accessibility
        store.ping()
        return {"status": "ready"}
    except Exception as e:
        return JSONResponse(status_code=503, content={"status": "not-ready", "error": str(e)})


@app.get("/api/info")
def info():
    hostname = socket.gethostname()
    return {
        "app": "course-app",
        "hostname": hostname,
        "store": store.name,
        "db_path": DB_PATH,
        "redis_url": REDIS_URL if getattr(store, 'name', '') == 'redis' else "",
        "messages_api": MESSAGES_API if getattr(store, 'name', '') == 'http' else "",
        "counter_api": COUNTER_API if getattr(store, 'name', '') == 'http' else "",
        "message": APP_MESSAGE,
        "secret_token_present": bool(SECRET_TOKEN),
        "env": {k: v for k, v in os.environ.items() if k.startswith("APP_")},
    }


@app.get("/api/messages")
def get_messages(limit: int = 20):
    return {"items": store.list_messages(limit=limit)}


@app.post("/api/messages")
def post_message(text: str | None = Form(None), qtext: str | None = Query(None)):
    # Accept both form-encoded (preferred) and query param for flexibility
    t = text or qtext
    if not t or not t.strip():
        raise HTTPException(status_code=400, detail="text is required")
    store.add_message(t.strip())
    return {"status": "created"}


def _burn_cpu(seconds: int):
    end = time.time() + seconds
    x = 0.0001
    while time.time() < end:
        x = math.sqrt(x) ** 2 + math.sin(x)  # meaningless math


@app.get("/stress")
def stress(seconds: int = 10, background: bool = True):
    seconds = max(1, min(seconds, 120))
    if background:
        t = threading.Thread(target=_burn_cpu, args=(seconds,), daemon=True)
        t.start()
        return {"status": "started", "seconds": seconds}
    else:
        _burn_cpu(seconds)
        return {"status": "done", "seconds": seconds}
