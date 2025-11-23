# Simple Go App Docker

This project contains a Go application and a Dockerfile using **multi-stage build** and a **non-root user**.

---

## 🛠 Build Docker image

#### From the project root:

```bash
docker build -f homeworks/yarovskyi/module-2/lesson-03/Dockerfile -t simple-app-multi-stage .
```
#### Check image size:
```bash
docker images simple-app-multi-stage
```
Example output:
```
REPOSITORY               TAG       IMAGE ID       CREATED          SIZE
simple-app-multi-stage   latest    5013c660735a   15 minutes ago   20.2MB
```
#### Build stage "build-app":
```bash
docker build -f homeworks/yarovskyi/module-2/lesson-03/Dockerfile --target build-app -t simple-app-multi-stage-builder .
```
#### Check image size:
```bash
docker images simple-app-multi-stage-builder
```
Example output:
```
REPOSITORY                       TAG       IMAGE ID       CREATED          SIZE
simple-app-multi-stage-builder   latest    66a133e05d75   19 minutes ago   316MB
```

## 🏃 Run Docker container

```bash
docker run -d -p 8080:8080 simple-app-multi-stage
```

Open in browser: [http://localhost:8080](http://localhost:8080)

## ✅ Verify non-root user

```bash
docker run -it --entrypoint /bin/sh simple-app-multi-stage
>whoami
>id
```
Example output:
```
/app $ whoami
appuser
/app $ id
uid=1000(appuser) gid=1000(appuser) groups=1000(appuser)
```

## 📦 Docker HUB

#### Tag local image with remote key:
```bash
docker tag simple-app-multi-stage yarovskiy/simple-app-multi-stage
```
#### Login to Docker HUB:
```bash
docker login
```
#### Push linked image to HUB:
```bash
docker push yarovskiy/simple-app-multi-stage
```
Link: https://hub.docker.com/repository/docker/yarovskiy/simple-app-multi-stage/general
#### Pull image:
```bash
docker pull yarovskiy/simple-app-multi-stage
```
or run directly:
```bash
docker run -d -p 8080:8080 yarovskiy/simple-app-multi-stage
```
