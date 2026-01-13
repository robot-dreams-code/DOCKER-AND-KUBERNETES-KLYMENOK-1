Написати Dockerfile для apps/simple-app.

1. Створюємо базовий актуальний образ. Важить він 316MB.

FROM golang:alpine AS build # Використаєм легкий образ із golang
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download	# Завантаження залежностей. Кешуємо цей шар.

COPY . .
RUN go build -o app main.go # Білдимо апку

2. Створимо multi stage образ. За основу беремо наш build. Такий образ займає всього 11.9MB, тому що ми не тягнемо із собою залежності go, а копіюємо лише бінарник з build.

FROM scratch
COPY --from=build --chown=1000:1000 /app/app /app  # Використовуємо build. 
USER 1000
EXPOSE 8080
ENTRYPOINT ["/app"]

Окрему увагу слід виділити на визначення non-root користувача. Так як Scratch це пуста оболонка, вона не має башу і базових лінукс утиліт. Тому ми не можемо використати useradd. Рішення знайшов тут https://www.reddit.com/r/docker/comments/9ussty/security_risk_of_running_a_scratch_container/. Всі лінукс контейнери ряняться як uid=0 (root). Тому визначаємо USER 1000, таким чином юзер не рут.

Білдимо імедж:
docker build -t simple-app-multi-stage .

Мапимо 8080 порт і ранимо контейнер: (до речі, важливо спочатку вказати порт, а після - назву імеджа)
docker run -p 8080:8080 simple-app-multi-stage

3. Тегнемо наш імедж і запушимо на dockerhub.

docker tag simple-app-multi-stage dmytrokain/simple-app-multi-stage:v1
docker push dmytrokain/simple-app-multi-stage:v1

https://hub.docker.com/r/dmytrokain/simple-app-multi-stage - Імедж запушено.

