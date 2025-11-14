# module-02/lesson-04 – Viktor Petrushenko

Docker Compose для `course-app` з Redis.

## Файли:
- `Dockerfile`
- `docker-compose.yml`
- `data/`

## Перевірка:
```bash
docker compose up -d --build
curl http://localhost:8080/healthz
# → {"status":"ok"}
