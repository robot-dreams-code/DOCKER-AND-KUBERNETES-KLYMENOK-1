# Lesson 04 App with Redis

This project contains a FastAPI application and Redis, running via Docker Compose.

## Configuration

- Redis password: `veryStrongPassword`
- FastAPI port: `8084`

Redis URL for the app: 
```
redis://:veryStrongPassword@redis:6379/0
```

## Running the project

1. Run command:

a) From the root directory:
```bash
docker compose -f homeworks/yarovskyi/module-2/lesson-04/docker-compose.yaml up -d
```

b) Or go to the lesson directory and run command:
```bash
cd homeworks/yarovskyi/module-2/lesson-04/
docker compose up -d
```
2. FastAPI will be available at: http://localhost:8084
3. Connect to Redis CLI:

a) If docker compose was started from the root directory:
```bash
docker compose -f homeworks/yarovskyi/module-2/lesson-04/docker-compose.yaml exec redis redis-cli -a veryStrongPassword
```

b) Or from the lesson directory:
```bash
docker compose exec redis redis-cli -a veryStrongPassword
```

And then run commands:
```bash
> KEYS *
> GET counters:visits
```
4. Stopping the project:

a) If docker compose was started from the root directory:
```bash
docker compose -f homeworks/yarovskyi/module-2/lesson-04/docker-compose.yaml down
```

b) Or from the lesson directory:
```bash
docker compose down
```
