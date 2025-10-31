#!/usr/bin/env bash
# Запускає контейнер nginx і відкриває порт 8080

docker run -d --name web-8080 -p 8080:80 nginx:latest