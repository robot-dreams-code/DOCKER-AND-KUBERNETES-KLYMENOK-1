# module-02/lesson-04 – Viktor Petrushenko

Docker Compose для `course-app` (без копіювання).

## Файли:
- `Dockerfile` ← копіює з `../../../apps/course-app/`
- `docker-compose.yml` ← `build: .`
- `data/`

## Перевірка:
```bash
docker compose up -d --build
curl http://localhost:8080/healthz
# → {"status":"ok"}
