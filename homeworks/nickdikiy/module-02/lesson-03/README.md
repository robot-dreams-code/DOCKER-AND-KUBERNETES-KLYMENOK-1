## 1. Створимо Dockerfile
### CGO_ENABLED=0 параметр потрібен для створення статично лінкованого бінарника
### .dockerignore файл має бути розміщений в корені контексті збірки. Ми додали туди README.md, це єдиний файл, який нам непотрібен для збірки образу.

## 2. Створимо images на основі Dockerfile:
### Використовуємо --target=build для того щоб вказати етап з multistage build.Параметр корисний коли нам потрібно "подебажити" контейнер, тому що нам не потрібно змінювати Dockerfile для запуску певного етапу.
```bash
docker build -f homeworks/nickdikiy/module-02/lesson-03/Dockerfile -t simple-app-no-optimized:1.0 ./apps/simple-app --target=build
docker build -f homeworks/nickdikiy/module-02/lesson-03/Dockerfile -t simple-app:1.0 ./apps/simple-app
```


## 2. Перевіримо розмір image:
```bash
docker images
```
```
REPOSITORY                TAG       IMAGE ID       CREATED          SIZE
simple-app                1.0       472fad020ea3   2 seconds ago    10.5MB
simple-app-no-optimized   1.0       b0121a2437c5   13 seconds ago   938MB
```
#### Так як ми запускаємо multistage build, image e7fb34e08de0 використовується повторно, docker його позначає як не потрібний, тому repository і tag = <none>


## 3. Запустимо контейнер (-d - detached mode, контейнер працює в фоні):
```bash
docker run -p 8080:8080 --name simple-app simple-app:1.0
docker run -d -p 8080:8080 --name simple-app simple-app:1.0
```
#### За посиланням http://localhost:8080/ можемо побачити симпатичну сторінку з домашнім завданням. Також ми знайшли додаткову інформацію про "Ідеї для експериментів" :) 



## 4. Перевіримо користувача:
```bash
 docker inspect -f '{{.Config.User}}' $(docker ps -aqf "name=simple-app" | head -n 1)
```
#### Бачимо що наш користувач 1000:1000. Також в контейнері немає абсолютно нічого крім нашого одного бінарника.



## 4. Перевіримо кількість шарів для кожного image:
```bash
docker history simple-app-no-optimized:1.0
dokcer history simple-app:1.0
```
```
IMAGE          CREATED              CREATED BY                SIZE      COMMENT
472fad020ea3   About a minute ago   CMD ["./app"]             0B        buildkit.dockerfile.v0
<missing>      About a minute ago   EXPOSE map[8080/tcp:{}]   0B        buildkit.dockerfile.v0
<missing>      About a minute ago   USER 1000:1000            0B        buildkit.dockerfile.v0
<missing>      About a minute ago   COPY app . # buildkit     10.5MB    buildkit.dockerfile.v0
```

```
IMAGE          CREATED         CREATED BY                                      SIZE      COMMENT
b0121a2437c5   2 minutes ago   RUN /bin/sh -c CGO_ENABLED=0 go build -o app…   92.2MB    buildkit.dockerfile.v0
<missing>      2 minutes ago   COPY . . # buildkit                             9.4kB     buildkit.dockerfile.v0
<missing>      2 minutes ago   RUN /bin/sh -c go mod tidy # buildkit           16.9kB    buildkit.dockerfile.v0
<missing>      2 minutes ago   COPY go.mod go.sum . # buildkit                 229B      buildkit.dockerfile.v0
<missing>      2 minutes ago   WORKDIR /app                                    0B        buildkit.dockerfile.v0
<missing>      3 months ago    WORKDIR /go                                     0B        buildkit.dockerfile.v0
<missing>      3 months ago    RUN /bin/sh -c mkdir -p "$GOPATH/src" "$GOPA…   0B        buildkit.dockerfile.v0
<missing>      3 months ago    COPY /target/ / # buildkit                      235MB     buildkit.dockerfile.v0
<missing>      3 months ago    ENV PATH=/go/bin:/usr/local/go/bin:/usr/loca…   0B        buildkit.dockerfile.v0
<missing>      3 months ago    ENV GOPATH=/go                                  0B        buildkit.dockerfile.v0
<missing>      3 months ago    ENV GOTOOLCHAIN=local                           0B        buildkit.dockerfile.v0
<missing>      3 months ago    E[README.md](README.md)NV GOLANG_VERSION=1.23.12                      0B        buildkit.dockerfile.v0
<missing>      3 months ago    RUN /bin/sh -c set -eux;  apt-get update;  a…   240MB     buildkit.dockerfile.v0
<missing>      22 months ago   RUN /bin/sh -c set -eux;  apt-get update;  a…   183MB     buildkit.dockerfile.v0
<missing>      2 years ago     RUN /bin/sh -c set -eux;  apt-get update;  a…   48.5MB    buildkit.dockerfile.v0
<missing>      2 years ago     # debian.sh --arch 'arm64' out/ 'bookworm' '…   139MB     debuerreotype 0.15
```

#### В фінальному образі simple-app:1.0 всього 4 шари, оптимізувати нічого. В simple-app-no-optimized:1.0 образі шарів більше, тому що ми використовуємо повний образ debian. Так як ми копіювали файли за принципом "чим рідше змінюється файл, тим вище він в dockerfile" шари кешу також оптимізовані.


## 5. Запушимо image:
```bash
docker login -u nickdikiynd
docker tag simple-app:1.0 nickdikiynd/simple-app:1.0
docker push nickdikiynd/simple-app:1.0    
```
```
The push refers to repository [docker.io/nickdikiynd/simple-app]
f0a91c00ec4b: Pushed 
1.0: digest: sha256:aa9ffb63d331162f5ebb2b508465ec865b3f4424d172c256630025aa9a45017b size: 527
```
## 6. Запустимо додаток з dockerhub:
```bash
docker pull nickdikiynd/simple-app:1.0
docker run -d -p 8080:8080 --name simple-app nickdikiynd/simple-app:1.0
dokcer ps
```
```
1.0: Pulling from nickdikiynd/simple-app
Digest: sha256:aa9ffb63d331162f5ebb2b508465ec865b3f4424d172c256630025aa9a45017b
Status: Image is up to date for nickdikiynd/simple-app:1.0
docker.io/nickdikiynd/simple-app:1.0

CONTAINER ID   IMAGE                        COMMAND   CREATED         STATUS         PORTS                                         NAMES
310a91e94e64   nickdikiynd/simple-app:1.0   "./app"   5 seconds ago   Up 5 seconds   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   simple-app
```
