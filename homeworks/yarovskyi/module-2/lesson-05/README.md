# Lesson 05 App with healthchecks and volumes

This project contains a FastAPI application and Redis, running via Docker Compose.

## Configuration

- Redis password: `veryStrongPassword`
- FastAPI port: `8085`

Redis URL for the app: 
```
redis://:veryStrongPassword@redis:6379/0
```

## Running the project

1. Run command:

a) From the root directory:
```bash
docker compose -f homeworks/yarovskyi/module-2/lesson-05/docker-compose.yaml up -d
```

b) Or go to the lesson directory and run command:
```bash
cd homeworks/yarovskyi/module-2/lesson-05/
docker compose up -d
```
2. FastAPI will be available at: http://localhost:8085
3. Connect to Redis CLI:

a) If docker compose was started from the root directory:
```bash
docker compose -f homeworks/yarovskyi/module-2/lesson-05/docker-compose.yaml exec redis redis-cli -a veryStrongPassword
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
docker compose -f homeworks/yarovskyi/module-2/lesson-05/docker-compose.yaml down
```

b) Or from the lesson directory:
```bash
docker compose down
```

## Docker Swarm

5. Init docker swarm
```bash
docker swarm init --advertise-addr 192.168.64.2 --listen-addr 0.0.0.0:2377
```

6. Deploy docker swarm
```bash
docker stack deploy -c homeworks/yarovskyi/module-2/lesson-05/docker-compose.swarm.yaml courseapp
```
Check stack:
```bash
docker stack services courseapp
```

7. Scale services:
```bash
docker service scale courseapp_app=3
```

8. Stopping docker swarm
```bash
docker swarm leave --force
```
