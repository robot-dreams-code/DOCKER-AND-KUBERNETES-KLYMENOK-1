lesson-04/
│
├─ docker-compose.yml
├─ apps\
│   └─ course-app\
│       ├─ Dockerfile
│       ├─ main.go
│       └─ README.md
└─ README.md

Запустити контейнері:
docker compose up -d --build

docker compose ps


Перевірка роботи

Головна сторінка:
http://localhost:8080/

Health check:
http://localhost:8080/healthz

docker compose exec redis redis-cli ping
# повинно повернути PONG