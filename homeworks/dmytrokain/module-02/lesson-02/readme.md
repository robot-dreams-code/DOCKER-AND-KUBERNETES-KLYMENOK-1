## homework(module-02/lesson-02): Dmytro Kayinskyy


### 1. Встановлено Rancher Desktop для Windows (Container Engine: Moby/dockerd).
Особливістю роботи Docker у Windows є те, що він використовує WSL (Windows Subsystem for Linux) для того, щоб запускати Linux контейнери.

Linux нативно використовує технологію Docker.  
Windows - через WSL.  
MacOS - через Lima/Colima VM та інші.

Всю подальшу роботу виконуватиму у WSL.

### 2. Запуск першого контейнеру hello-world.

Для створення образу за основу взяв busybox, який є досить легким і містить основні unix утиліти.

Cтворимо index.html з наступним вмістом:

`Hello World from my first minimalistic BusyBox container!`

Cтворимо Dockerfile:

```
FROM busybox
WORKDIR /hello_world
COPY index.html .
EXPOSE 8080

CMD ["busybox", "httpd", "-f", "-p", "8080"]
```

Збілдимо образ:  
`docker build -t hello_busybox_image .`

Запустимо в контейнер на основі цього образу промапимо порт 8080 з контейнера на порт 8080 назовні:

`docker run --name hello_container -p 8080:8080 hello_busybox_image`

Зайдемо на http://localhost:8080/ і побачимо наше повідомлення.

### 3. Запустити 10 контейнерів з образом nginx.

Для цього напишемо bash скрипт run_ten_containers.sh:
```
#!/bin/sh

for i in $(seq 1 10); do
  docker run -d --name nginx_container_$i nginx
done
```

Запустимо sh run_ten_containers.sh

Зупинимо контейнери:  
```docker stop $(docker ps -q --filter "name=nginx_container_")```  
Видалимо контейнери:  
```docker rm $(docker ps -q --filter "name=nginx_container_")```


