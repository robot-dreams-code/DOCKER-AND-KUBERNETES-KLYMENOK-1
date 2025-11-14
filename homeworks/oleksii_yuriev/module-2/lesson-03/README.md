# Simple App 🐳


## Build image
```bash
docker build --no-cache -t simple_app:1.0.4  -f homeworks/oleksii_yuriev/module-2/lesson-03/Dockerfile apps/simple-app
[+] Building 8.6s (14/14) FINISHED                                                                                                                                                           docker:rancher-desktop
 => [internal] load build definition from Dockerfile                                                                                                                                                           0.0s
 => => transferring dockerfile: 276B                                                                                                                                                                           0.0s
 => [internal] load metadata for docker.io/library/alpine:3.22                                                                                                                                                 1.0s
 => [internal] load metadata for docker.io/library/golang:1.23-alpine                                                                                                                                          0.9s
 => [internal] load .dockerignore                                                                                                                                                                              0.0s
 => => transferring context: 2B                                                                                                                                                                                0.0s
 => [build 1/4] FROM docker.io/library/golang:1.23-alpine@sha256:383395b794dffa5b53012a212365d40c8e37109a626ca30d6151c8348d380b5f                                                                              0.0s
 => [stage-1 1/4] FROM docker.io/library/alpine:3.22@sha256:4b7ce07002c69e8f3d704a9c5d6fd3053be500b7f1c69fc0d80990c2ad8dd412                                                                                   0.0s
 => [internal] load build context                                                                                                                                                                              0.0s
 => => transferring context: 241B                                                                                                                                                                              0.0s
 => CACHED [stage-1 2/4] WORKDIR /app                                                                                                                                                                          0.0s
 => CACHED [build 2/4] WORKDIR /app                                                                                                                                                                            0.0s
 => [stage-1 3/4] RUN adduser -D -u 1000 appuser                                                                                                                                                               0.2s
 => [build 3/4] COPY . .                                                                                                                                                                                       0.0s
 => [build 4/4] RUN go build -o simple-app main.go                                                                                                                                                             7.5s
 => [stage-1 4/4] COPY --from=build /app/simple-app ./                                                                                                                                                         0.0s
 => exporting to image                                                                                                                                                                                         0.0s
 => => exporting layers                                                                                                                                                                                        0.0s
 => => writing image sha256:0e64e350380fd7a03ea70d0cbfb62a761e545ae772bd2463f87d3fa57bfb3559                                                                                                                   0.0s
 => => naming to docker.io/library/simple_app:1.0.4

```

## Run Container
```bash
docker run -d --name test -p 8080:8080 simple_app:1.0.4

ed1e691ded174c6be96f5a81dee6d53e628cc152d786f5f34a77830406a3d081

```

## Check Running Container
```bash
docker ps
CONTAINER ID   IMAGE              COMMAND          CREATED          STATUS          PORTS                                         NAMES
ed1e691ded17   simple_app:1.0.4   "./simple-app"   34 seconds ago   Up 33 seconds   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   test
```

## Verify Running App
```bash
docker exec -it test sh
/app $
/app $
/app $ ps -ef
PID   USER     TIME  COMMAND
    1 appuser   0:00 ./simple-app
    9 appuser   0:00 sh
   15 appuser   0:00 ps -ef
/app $ netstat -tlnp
Active Internet connections (only servers)
Proto Recv-Q Send-Q Local Address           Foreign Address         State       PID/Program name
tcp        0      0 :::8080                 :::*                    LISTEN      1/simple-app
/app $
/app $
```


## Check
- http://localhost:8080
