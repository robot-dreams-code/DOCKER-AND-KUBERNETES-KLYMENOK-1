# Simple App 🐳


## Build image
```bash
docker build --no-cache -t lesson-04:1.0.0  -f homeworks/oleksii_yuriev/module-2/lesson-04/Dockerfile apps/course-app
[+] Building 9.2s (11/11) FINISHED                                                                                                                                                           docker:rancher-desktop
 => [internal] load build definition from Dockerfile                                                                                                                                                           0.0s
 => => transferring dockerfile: 322B                                                                                                                                                                           0.0s
 => [internal] load metadata for docker.io/library/python:3.14-alpine3.22                                                                                                                                      1.1s
 => [internal] load .dockerignore                                                                                                                                                                              0.0s
 => => transferring context: 2B                                                                                                                                                                                0.0s
 => [1/6] FROM docker.io/library/python:3.14-alpine3.22@sha256:8373231e1e906ddfb457748bfc032c4c06ada8c759b7b62d9c73ec2a3c56e710                                                                                0.0s
 => [internal] load build context                                                                                                                                                                              0.0s
 => => transferring context: 121B                                                                                                                                                                              0.0s
 => CACHED [2/6] WORKDIR /app                                                                                                                                                                                  0.0s
 => [3/6] COPY requirements.txt .                                                                                                                                                                              0.0s
 => [4/6] RUN pip install -r requirements.txt                                                                                                                                                                  7.6s
 => [5/6] COPY . .                                                                                                                                                                                             0.0s
 => [6/6] RUN adduser -D -u 1000 appuser      && chown -R appuser:appuser /app                                                                                                                                 0.2s
 => exporting to image                                                                                                                                                                                         0.2s
 => => exporting layers                                                                                                                                                                                        0.2s
 => => writing image sha256:170ab5b32f65ad76cf9a8a9020cd909c94bb0db6b8c0e1fd2edf7533306fdb1d                                                                                                                   0.0s
 => => naming to docker.io/library/lesson-04:1.0.0

```

## Run Container
```bash
docker-compose  -f homeworks/oleksii_yuriev/module-2/lesson-04/docker-compose.yml up -d
```

## Check Running Container
```bash
docker ps                                                                                                                                    9s
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                                         NAMES
d4a9450b0782   d857e4341f99   "uvicorn src.main:ap…"   7 minutes ago   Up 7 minutes   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   lesson-04-app-1
a4e16401b1f4   redis:alpine   "docker-entrypoint.s…"   7 minutes ago   Up 7 minutes   6379/tcp                                      lesson-04-redis-1

```

## Check App
```bash
curl localhost:8080/healthz
{"status":"ok"}%

```
