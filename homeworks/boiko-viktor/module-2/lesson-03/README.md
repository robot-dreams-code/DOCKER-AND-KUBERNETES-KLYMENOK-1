# Збірка імеджа nonroot при умові що знаходимось в дерикторії уроку
`buildx build --platform linux/amd64,linux/arm64  -t viktor1sss/goapp:nonroot -f Dockerfile.nonroot  ../../../../apps/simple-app --push`

# Збірка імеджа scratch при умові що знаходимось в дерикторії уроку
`buildx build --platform linux/amd64,linux/arm64  -t viktor1sss/goapp:scratch -f Dockerfile.scratch  ../../../../apps/simple-app --push`

# Запуск контейнерів на порту 8080-8081
`docker run -p 8080:8080 viktor1sss/goapp:nonroot`
`docker run -p 8081:8080 viktor1sss/goapp:scratch`

# Посилання на репозиторій:
https://hub.docker.com/r/viktor1sss/goapp/tags
