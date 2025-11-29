# robot_dreams :: Lessons-05

## Overview

В основний Dockerfile додано інструкції встановлення залежних пакетів:
```
...
RUN apk update && \
    apk add curl jq && \
    rm -rf /var/cache/apk/*
...
```

А в сам docker compose додано выдповыдны ынструкції:

```
services:
  python:
    ...
    healthcheck:
      test: ["CMD-SHELL", "curl -s http://localhost:8080/healthz | jq -e '.status == \"ok\"' || exit 1"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 10s
    depends_on:
      - redis
```

Це дозволить додатково опрацювати перевірку health-check і навіть сприймати відповідний статус респонсу:

```bash
curl http://localhost:8080/healthz

{"status":"ok"}
```

Перегляд статусу перевірки healthcheck:

```bash
docker inspect --format "{{json .State.Health }}" lesson-05-python-1 | jq
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "2025-11-20T17:34:06.760578232+02:00",
      "End": "2025-11-20T17:34:06.809252745+02:00",
      "ExitCode": 0,
      "Output": "true\n"
    }
  ]
}
```

Можна, джля перевірки, прописати заздалегідь некоректний статус перевірки (`... jq -e '.status == \"x-ok\"' ...`) і побачити як відпрацює Docker Healthcheck:

```bash
docker inspect --format "{{json .State.Health }}" lesson-05-python-1 | jq
{
  "Status": "starting",
  "FailingStreak": 2,
  "Log": [
    {
      "Start": "2025-11-20T17:33:07.692496634+02:00",
      "End": "2025-11-20T17:33:07.732934344+02:00",
      "ExitCode": 1,
      "Output": "false\n"
    },
    {
      "Start": "2025-11-20T17:33:12.734574522+02:00",
      "End": "2025-11-20T17:33:12.766710673+02:00",
      "ExitCode": 1,
      "Output": "false\n"
    },
    {
      "Start": "2025-11-20T17:33:42.768290673+02:00",
      "End": "2025-11-20T17:33:42.806756579+02:00",
      "ExitCode": 1,
      "Output": "false\n"
    }
  ]
}
```