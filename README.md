# FastAPI Service (Steps 1–5 Completed)

## Local run
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --host 0.0.0.0 --port 8080
```

## Docker run
```bash
docker build -t my-fastapi:latest .
docker run --rm -p 8080:8080 my-fastapi:latest
```
