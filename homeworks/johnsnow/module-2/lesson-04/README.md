# Homework: Module 02 / Lesson 04

## Docker Compose

### Запуск
```bash
docker compose -f DOCKER-AND-KUBERNETES-KLYMENOK-1/homeworks/klymenko-oleksandr/module-2/lesson-04/docker-compose.yaml up -d --build
```

### Перевірка
```bash
curl http://localhost:8080/healthz
curl http://localhost:8080/api/info
```

### Зупинка та очищення контейнерів
```bash
docker compose down
```