# homework(module-02/lesson-03): Volodymyr Chornonoh

## Pre-requisites

```bash
cp homeworks/chornonoh/module-02/lesson-03/.dockerignore \
    apps/simple-app/.dockerignore
```

`.dockerignore` file must be in the build context

## Building the image

```bash
docker build \
    -f homeworks/chornonoh/module-02/lesson-03/Dockerfile \
    -t simple-app \
    apps/simple-app
```

## Tagging and pushing

```bash
docker tag simple-app hbvhuwe/simple-app:latest
docker push hbvhuwe/simple-app:latest
```

## Running

Local image:

```bash
docker run -p 18080:8080 simple-app:latest
```

Image from the registry:

```bash
docker run -p 18080:8080 hbvhuwe/simple-app:latest
```

## Size comparison

Build-only stage:

```bash
docker build \
    -f homeworks/chornonoh/module-02/lesson-03/Dockerfile \
    -t simple-app-build \
    --target build \
    apps/simple-app
```

```bash
docker image ls --filter "reference=simple-app*"
```

```txt
REPOSITORY         TAG       IMAGE ID       CREATED          SIZE
simple-app-build   latest    1abcf0bd958b   10 seconds ago   938MB
simple-app         latest    b4b06d8bbc56   18 minutes ago   10.5MB
```
