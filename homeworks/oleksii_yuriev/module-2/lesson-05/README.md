# Simple App 🐳


## Build image
```bash
docker build --no-cache -t lesson-05:1.0.0  -f homeworks/oleksii_yuriev/module-2/lesson-05/Dockerfile apps/course-app
[+] Building 10.6s (11/11) FINISHED                                                                                                                                                          docker:rancher-desktop
 => [internal] load build definition from Dockerfile                                                                                                                                                           0.0s
 => => transferring dockerfile: 362B                                                                                                                                                                           0.0s
 => [internal] load metadata for docker.io/library/python:3.14-alpine3.22                                                                                                                                      1.1s
 => [internal] load .dockerignore                                                                                                                                                                              0.0s
 => => transferring context: 2B                                                                                                                                                                                0.0s
 => [1/6] FROM docker.io/library/python:3.14-alpine3.22@sha256:8373231e1e906ddfb457748bfc032c4c06ada8c759b7b62d9c73ec2a3c56e710                                                                                0.0s
 => [internal] load build context                                                                                                                                                                              0.0s
 => => transferring context: 121B                                                                                                                                                                              0.0s
 => CACHED [2/6] WORKDIR /app                                                                                                                                                                                  0.0s
 => [3/6] COPY requirements.txt .                                                                                                                                                                              0.0s
 => [4/6] RUN pip install -r requirements.txt                                                                                                                                                                  7.5s
 => [5/6] COPY . .                                                                                                                                                                                             0.0s
 => [6/6] RUN adduser -D -u 1000 appuser      && chown -R appuser:appuser /app      &&  apk update && apk add curl                                                                                             1.7s
 => exporting to image                                                                                                                                                                                         0.2s
 => => exporting layers                                                                                                                                                                                        0.2s
 => => writing image sha256:16aa052fa132e335e8576527c219372239e7e1cf97ef82a086399014df475bca                                                                                                                   0.0s
 => => naming to docker.io/library/lesson-05:1.0.0
```

## Run Container
```bash
docker-compose  -f homeworks/oleksii_yuriev/module-2/lesson-05/docker-compose.yml up -d
```

## Check Running Container
```bash
docker ps
CONTAINER ID   IMAGE             COMMAND                  CREATED         STATUS                   PORTS                                         NAMES
bd07960bec5e   lesson-05:1.0.0   "uvicorn src.main:ap…"   2 minutes ago   Up 2 minutes (healthy)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   lesson-05-app-1
bb9426b5c301   redis:alpine      "docker-entrypoint.s…"   2 minutes ago   Up 2 minutes (healthy)   6379/tcp                                      lesson-05-redis-1

```

## Check App
```bash
curl localhost:8080/healthz
{"status":"ok"}%

```
