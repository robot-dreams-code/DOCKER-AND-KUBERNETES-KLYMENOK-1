Отже, мульти-стейдж в рази зменшив розмір образу

Мульти стейдж образ з alpine раннером
simplego                                            v1.0                   20588796e4a9   6 minutes ago    19.4MB
Сінгл стейдж образ з FROM golang:1.23
simplego                                            v1.0                   842a39f0d3d3   6 seconds ago   939MB
Сінгл стейдж образ з FROM golang:1.23-alpine (в нього немає useradd і потрібно встановити окремо)
simplego                                            v1.0                   860efa33ee38   5 seconds ago   342MB

Запушив у (попередньо створений) репозиторій DockerHub (забув tagname поміняти, але нехай вже буде)
docker tag simplego:v1.0 andreqko/simplego:tagname
docker push andreqko/simplego:tagname

https://hub.docker.com/repository/docker/andreqko/simplego/general

Спулив через docker pull andreqko/simplego:tagname і образ зʼявився в docker images
