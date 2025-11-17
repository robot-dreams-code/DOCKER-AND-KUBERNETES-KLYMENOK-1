### Size of the image is 935MB, which is too big.
```
dtimchuk@dt DOCKER-AND-KUBERNETES-KLYMENOK-1 % docker build -f homeworks/dtimchuk/module-2/lesson-03/Dockerfile -t simple-app .
[+] Building 19.7s (10/10) FINISHED                                                                                                             docker:rancher-desktop
=> [internal] load build definition from Dockerfile                                                                                                              0.0s
=> => transferring dockerfile: 901B                                                                                                                              0.0s
=> [internal] load metadata for docker.io/library/golang:1.23                                                                                                    1.6s
=> [auth] library/golang:pull token for registry-1.docker.io                                                                                                     0.0s
=> [internal] load .dockerignore                                                                                                                                 0.0s
=> => transferring context: 2B                                                                                                                                   0.0s
=> [1/4] FROM docker.io/library/golang:1.23@sha256:60deed95d3888cc5e4d9ff8a10c54e5edc008c6ae3fba6187be6fb592e19e8c0                                             11.6s
=> => resolve docker.io/library/golang:1.23@sha256:60deed95d3888cc5e4d9ff8a10c54e5edc008c6ae3fba6187be6fb592e19e8c0                                              0.0s
=> => sha256:ac2b6b754dbe064bd10a97c2f46f9253a5e8220565fc3ae4edf8b362b87bbe2f 2.33kB / 2.33kB                                                                    0.0s
=> => sha256:0ea54978ec8888bd907c0b0d552b4ac12dd5951ddc37fead577d17d7252e2f91 2.82kB / 2.82kB                                                                    0.0s
=> => sha256:6fbab1970a5a8545cb921278645cd2e79f4eb23c4bdfb714bef2fdf569acddd0 48.34MB / 48.34MB                                                                  1.9s
=> => sha256:e4b341315eac0ea1ad859055038b69990fff352cc7f160586e6a94f1b126675d 23.56MB / 23.56MB                                                                  2.0s
=> => sha256:60deed95d3888cc5e4d9ff8a10c54e5edc008c6ae3fba6187be6fb592e19e8c0 9.75kB / 9.75kB                                                                    0.0s
=> => sha256:1de51daaef2003ecaec3c73f5ef373c01bb10f38b5ec85db7d9077efa7231264 64.36MB / 64.36MB                                                                  3.7s
=> => extracting sha256:6fbab1970a5a8545cb921278645cd2e79f4eb23c4bdfb714bef2fdf569acddd0                                                                         1.7s
=> => sha256:9e9120ca78766d83c8bf471f4ebcf188411560b50a1ea974defebed9817214bc 86.43MB / 86.43MB                                                                  5.8s
=> => sha256:382d65ac76ebcbc7ba7ee0d232ae7afbec48e2b3b673983ac8ced522dabe3abb 70.70MB / 70.70MB                                                                  5.1s
=> => sha256:3ac8581e911eebe7d8ccc07d02027616e59d9509699acbf7b23d56ced142b27b 126B / 126B                                                                        4.1s
=> => extracting sha256:e4b341315eac0ea1ad859055038b69990fff352cc7f160586e6a94f1b126675d                                                                         0.4s
=> => sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1 32B / 32B                                                                          4.4s
=> => extracting sha256:1de51daaef2003ecaec3c73f5ef373c01bb10f38b5ec85db7d9077efa7231264                                                                         2.0s
=> => extracting sha256:9e9120ca78766d83c8bf471f4ebcf188411560b50a1ea974defebed9817214bc                                                                         1.8s
=> => extracting sha256:382d65ac76ebcbc7ba7ee0d232ae7afbec48e2b3b673983ac8ced522dabe3abb                                                                         3.2s
=> => extracting sha256:3ac8581e911eebe7d8ccc07d02027616e59d9509699acbf7b23d56ced142b27b                                                                         0.0s
=> => extracting sha256:4f4fb700ef54461cfa02571ae0db9a0dc1e0cdb5577484a6d75e68dc38e8acc1                                                                         0.0s
=> [internal] load build context                                                                                                                                 0.0s
=> => transferring context: 428B                                                                                                                                 0.0s
=> [2/4] WORKDIR /usr/src/app                                                                                                                                    0.1s
=> [3/4] COPY apps/simple-app ./                                                                                                                                 0.0s
=> [4/4] RUN go build -o /usr/local/bin/app ./main.go                                                                                                            6.2s
=> exporting to image                                                                                                                                            0.2s
=> => exporting layers                                                                                                                                           0.2s
=> => writing image sha256:920bb59d7b126bea4c2af25eaf2c762049b12a657fd4464194ebee638ba9b614                                                                      0.0s
=> => naming to docker.io/library/simple-app                                                                                                                     0.0s

dtimchuk@dt DOCKER-AND-KUBERNETES-KLYMENOK-1 % docker images                                                                   
REPOSITORY                                          TAG                    IMAGE ID       CREATED         SIZE
simple-app                                          latest                 35a3c38f6045   2 minutes ago   935MB
```

### Size of the image is 10.6MB, which is acceptable.
```
dtimchuk@dt DOCKER-AND-KUBERNETES-KLYMENOK-1 % docker images                                                                   
dtimchuk@dt DOCKER-AND-KUBERNETES-KLYMENOK-1 % docker build -f homeworks/dtimchuk/module-2/lesson-03/Dockerfile -t simple-app .
[+] Building 0.2s (10/10) FINISHED                                                                                                              docker:rancher-desktop
=> [internal] load build definition from Dockerfile                                                                                                              0.0s
=> => transferring dockerfile: 958B                                                                                                                              0.0s
=> [internal] load metadata for docker.io/library/golang:1.23                                                                                                    0.2s
=> [internal] load .dockerignore                                                                                                                                 0.0s
=> => transferring context: 2B                                                                                                                                   0.0s
=> [stage-build 1/4] FROM docker.io/library/golang:1.23@sha256:60deed95d3888cc5e4d9ff8a10c54e5edc008c6ae3fba6187be6fb592e19e8c0                                  0.0s
=> [internal] load build context                                                                                                                                 0.0s
=> => transferring context: 428B                                                                                                                                 0.0s
=> CACHED [stage-build 2/4] WORKDIR /usr/src/app                                                                                                                 0.0s
=> CACHED [stage-build 3/4] COPY apps/simple-app ./                                                                                                              0.0s
=> CACHED [stage-build 4/4] RUN go build -o /usr/local/bin/app ./main.go                                                                                         0.0s
=> CACHED [stage-1 1/1] COPY --from=stage-build . .                                                                                                              0.0s
=> exporting to image                                                                                                                                            0.0s
=> => exporting layers                                                                                                                                           0.0s
=> => writing image sha256:35a3c38f6045e4dab13624aa2878015d3affc582e711b5c671aa76822c53c04e                                                                      0.0s
=> => naming to docker.io/library/simple-app

dtimchuk@dt DOCKER-AND-KUBERNETES-KLYMENOK-1 % docker images                                                                   
REPOSITORY                                          TAG                    IMAGE ID       CREATED          SIZE
simple-app                                          latest                 599527194472   16 seconds ago   10.6MB
```

### Run docker image
```
dtimchuk@dt DOCKER-AND-KUBERNETES-KLYMENOK-1 % docker run -d -p 8080:8080 --name test-simple-app simple-app  
a8fd1de24147fc82832cbe0ad17b7eeb0d3068312dee6816ecd196a9d66f78a6
```

### Steps for upload image to docker hub
#### 1. Login
`docker login`

#### 2. Make build
`docker build -f homeworks/dtimchuk/module-2/lesson-03/Dockerfile -t simple-app .`

#### 3. Add tag
`docker tag simple-app dmitrytimchuk/simple-app:latest`

#### 4. Push to docker hub
`docker push dmitrytimchuk/simple-app:latest`

### 5. Verification
`docker rmi dmitrytimchuk/simple-app:latest`
`docker rmi simple-app`

#### 6. Run from a registry
`docker pull dmitrytimchuk/simple-app:latest`
`docker run -d -p 8080:8080 --name test dmitrytimchuk/simple-app:latest`

#### 7. Test
`curl http://localhost:8080/health`

```
dtimchuk@dt DOCKER-AND-KUBERNETES-KLYMENOK-1 % docker ps
CONTAINER ID   IMAGE                        COMMAND                  CREATED          STATUS          PORTS                                         NAMES
668873fe17d7   simple-app                   "app -port 8080"         38 seconds ago   Up 37 seconds   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   simple-app-test
```

```aiignore
dtimchuk@dt DOCKER-AND-KUBERNETES-KLYMENOK-1 % curl http://localhost:8080                                          
<!DOCTYPE html>
<html lang="uk">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Застосунок для вивчення Docker</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<body>
    <div class="container">
        <header class="header">
            <h1>Створення та керування Docker-образами</h1>
            <div class="version-badge">Версія: 1.0.0</div>
        </header>

        <main class="content">
            <div class="card gradient-1">
                <h2>Ваше завдання</h2>
                <p>Створіть Dockerfile для цього застосунку</p>
            </div>

            <div class="card gradient-2">
                <h2>Про застосунок</h2>
                <p class="challenge-text">
                    Це простий веб-застосунок на Go, який демонструє основні концепції роботи з Docker
                    <br><br>
                    Застосунок складається з Go коду, HTML шаблонів та CSS стилів
                    <br><br>
                    Можете змінювати будь-які файли та перебудовувати Docker образ
                </p>
            </div>

            <div class="card gradient-3">
                <h2>Що варто реалізувати</h2>
                <ul class="practices-list">
                    <li>Використати multi-stage builds для зменшення розміру образу</li>
                    <li>Запускати від імені non-root користувача для безпеки</li>
                    <li>Використати кешування шарів правильно впорядковуючи команди</li>
                    <li>Використати конкретні версії базових образів (уникати 'latest')</li>
                    <li>Мінімізувати кількість шарів</li>
                    <li>Використати .dockerignore для виключення зайвих файлів</li>
                </ul>
            </div>

            <div class="experiment-section">
                <h3>Ідеї для експериментів</h3>
                <ol>
                    <li>Змініть цей текст і перебудуйте образ - зверніть увагу які кроки кешуються</li>
                    <li>Спробуйте змінити версію залежності в go.mod</li>
                    <li>Порівняйте розміри образів з multi-stage builds та без них</li>
                    <li>Перевірте, від імені якого користувача працює застосунок всередині контейнера</li>
                </ol>
            </div>
        </main>

        <footer class="footer">
            <p>Успіхів!</p>
        </footer>
    </div>
</body>
</html>
```