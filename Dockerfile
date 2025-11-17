#Назва шару totalbld
FROM golang:1.25.3-alpine AS totalbld

#Одразу створюємо юзера no-root
RUN adduser -D go-app-user

# поточна директорія
WORKDIR /pvk


COPY go.mod go.sum ./

RUN go mod download

COPY . .

# Збірка модуля з розташуванням в go-app/mygo-app
RUN go build -o /go-app/mygo-app ./main.go


# другий шар - сюди копіюємо тільки готовий модуль і права юзера
FROM scratch

# Копіюємо з правами root (з правами юзера не вдалось - була помилка)
COPY --from=totalbld /go-app/mygo-app /go-app/mygo-app
COPY --from=totalbld /etc/passwd /etc/passwd


USER go-app-user

EXPOSE 8080

# запуск
CMD ["/go-app/mygo-app"]
