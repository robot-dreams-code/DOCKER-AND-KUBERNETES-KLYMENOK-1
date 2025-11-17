# homework(module-02/lesson-05): Volodymyr Chornonoh

## Building and running with docker compose

```bash
docker compose build && docker compose up -d
```

## Checking status

```bash
 docker ps --filter name=lesson-05
```

Example output:

```txt
CONTAINER ID   IMAGE                  COMMAND                  CREATED          STATUS                    PORTS                                         NAMES
2e8adac2a896   lesson-05-course-app   "uvicorn src.main:ap…"   56 seconds ago   Up 44 seconds (healthy)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   lesson-05-course-app-1
fb43b06513b1   redis:8.2.3            "docker-entrypoint.s…"   6 minutes ago    Up 55 seconds (healthy)   6379/tcp                                      lesson-05-database-1
```

## Checking container health

```bash
docker inspect --format='{{json .State.Health}}' lesson-05-course-app-1 | jq
```

Example output:

```json
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "2025-11-17T11:22:20.025727698+02:00",
      "End": "2025-11-17T11:22:20.117750823+02:00",
      "ExitCode": 0,
      "Output": "{\"status\":\"ok\"}"
    },
    {
      "Start": "2025-11-17T11:22:30.118294537+02:00",
      "End": "2025-11-17T11:22:30.19219312+02:00",
      "ExitCode": 0,
      "Output": "{\"status\":\"ok\"}"
    },
    {
      "Start": "2025-11-17T11:22:40.193985458+02:00",
      "End": "2025-11-17T11:22:40.26158375+02:00",
      "ExitCode": 0,
      "Output": "{\"status\":\"ok\"}"
    }
  ]
}
```

```bash
docker inspect --format='{{json .State.Health}}' lesson-05-database-1 | jq
```

Example output:

```json
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "2025-11-17T11:22:29.354565245+02:00",
      "End": "2025-11-17T11:22:29.43251437+02:00",
      "ExitCode": 0,
      "Output": "PONG\n"
    },
    {
      "Start": "2025-11-17T11:22:39.434496541+02:00",
      "End": "2025-11-17T11:22:39.513061208+02:00",
      "ExitCode": 0,
      "Output": "PONG\n"
    },
    {
      "Start": "2025-11-17T11:22:49.514013421+02:00",
      "End": "2025-11-17T11:22:49.594176379+02:00",
      "ExitCode": 0,
      "Output": "PONG\n"
    },
    {
      "Start": "2025-11-17T11:22:59.595802467+02:00",
      "End": "2025-11-17T11:22:59.676540551+02:00",
      "ExitCode": 0,
      "Output": "PONG\n"
    },
    {
      "Start": "2025-11-17T11:23:09.677228847+02:00",
      "End": "2025-11-17T11:23:09.774179305+02:00",
      "ExitCode": 0,
      "Output": "PONG\n"
    }
  ]
}
```

## Initializing swarm

```bash
docker swarm init --advertise-addr 192.168.5.15
```

## Deploying stack

```bash
docker stack deploy -c stack.yaml lesson-05-stack
```

## Checking stack status

```bash
docker stack services lesson-05-stack
```

Example output:

```txt
ID             NAME                         MODE         REPLICAS   IMAGE                                 PORTS
dkdj0vax3xhw   lesson-05-stack_course-app   replicated   3/3        hbvhuwe/lesson-05-course-app:latest   *:8080->8080/tcp
vzj6zmlv2v89   lesson-05-stack_database     replicated   1/1        redis:8.2.3
```

## Scaling service

```bash
docker service scale lesson-05-stack_course-app=5
```

Status output:

```txt
ID             NAME                         MODE         REPLICAS   IMAGE                                 PORTS
dkdj0vax3xhw   lesson-05-stack_course-app   replicated   5/5        hbvhuwe/lesson-05-course-app:latest   *:8080->8080/tcp
vzj6zmlv2v89   lesson-05-stack_database     replicated   1/1        redis:8.2.3
```
