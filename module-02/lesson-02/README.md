
1. Встановлено Rancher Desktop (Container Engine: Moby/dockerd).
2. Перевірено роботу Docker:
   ```bash
   docker run --rm hello-world
3. Запущено веб-контейнер:
    docker run -d --name web-8080 -p 8080:80 nginx:latest
    Перевірено — http://localhost:8080
4. Автоматизовано запуск 10 контейнерів:
    for i in $(seq 1 10); do docker run -d --name "nginx-$i" -p $((8080+i)):80 nginx:latest; done
5. Зупинено та видалено всі запущені контейнери:
    docker rm -f $(docker ps -q)
