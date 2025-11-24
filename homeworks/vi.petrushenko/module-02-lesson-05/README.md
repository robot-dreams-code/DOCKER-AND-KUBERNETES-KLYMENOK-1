# module-02/lesson-05 – Viktor Petrushenko

- Healthcheck для `course-app` і `redis`  
- Том `appdata` → лічильник зберігається між перезапусками  
- `depends_on` + `condition: service_healthy`  
- Готовий до Swarm (`deploy`, named volumes)  

Перевірка стійкості:
```bash
docker compose up -d
curl http://localhost:8080   # → 1
curl http://localhost:8080   # → 2
docker compose down
docker compose up -d
curl http://localhost:8080   # → 3 (не скинувся!)

