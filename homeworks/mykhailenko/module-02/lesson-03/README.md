### Homework

Використав образ golang:1.25.0-alpine3.22, через те, наскільки легкий Alpine, та через завчасно встановлений Go. Для stage "target" використав Scratch, щоби вага образу була максимально мала. Сам image закинув в [Docker Hub](https://hub.docker.com/repository/docker/mmykhailenko/lesson-03/general).

Scratch зробив image приємно легшим

```

REPOSITORY                     TAG          IMAGE ID   CREATED     SIZE

mmykhailenko/lesson-03               latest        265611309137 34 minutes ago 11.9MB

mmykhailenko/lesson-03               build         af492a43590d 42 minutes ago 327MB

```

З цікавого, хотів створити daemon користувача, але вже такий існує в базовому образі, тому створив нового (deploy). Окрім того, довелось трохи поборотись з кешем. В мене в stage "build" прописана команда `RUN go build -o binary`. Вона виконувалась завжди, навіть якщо зміни були тільки в Dockerfile (навіть, якщо зміни були в stage "target"). Зробив `docker build --target build` й побачив, що Dockerfile попадав в сам образ й через це Docker оминав кеш для RUN, .dockerignore вирішив проблему😄

Також створив Dockerfile.dev щоби впевнитись, що процес йде під deploy:

```

admin simple-app % docker run -d mmykhailenko/lesson-03:dev

1fcf662de1ee9a22e17a267c648bae4b8a3e75fa750e07ca2cc2e01910632240

admin simple-app % docker exec -it 1fc /bin/sh

/app $ ls -l

-r-x------  1 deploy  deploy  11849123 Nov 9 10:25 binary

-rwx------  1 deploy  deploy     66 Nov 8 14:17 go.mod

-rwx------  1 deploy  deploy     163 Nov 8 14:17 go.sum

-rwx------  1 deploy  deploy    1529 Nov 8 16:35 main.go

drwx------  2 deploy  deploy    4096 Nov 8 16:35 static

drwx------  2 deploy  deploy    4096 Nov 8 16:35 templates

/app $ ps

PID  USER   TIME COMMAND

  1 deploy  0:00 /app/binary

  10 deploy  0:00 /bin/sh

  17 deploy  0:00 ps

/app $ 

```

P.S.

Ще знайшов 2 способи, як запустити додаток не створюючи image, використовуючи одну команду:

1. `docker run -p 8080:8080 -v $(pwd):/go/data --workdir /go/data golang go run main.go`.
2. `docker run -p 8080:8080 -v $(pwd):/go/data golang /bin/sh -c 'cd data && go run main.go'`
