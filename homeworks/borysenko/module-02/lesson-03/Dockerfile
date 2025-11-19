FROM golang:1.23 as build
WORKDIR /app

COPY ./apps/simple-app/go.mod ./apps/simple-app/go.sum ./
RUN go mod download

COPY ./apps/simple-app/ .

RUN CGO_ENABLED=0 go build -o /app/simple-app main.go

FROM alpine:3.22

##Дізнався що useradd не працює в alpine - а треба adduser. Спочатку робив через scratch але там взагалі ще важче бо ніби почитав що там немає системних adduser or useradd
RUN adduser -D app

WORKDIR /app

#Копіюю створений build після першого виконання
COPY --from=build /app/simple-app /app/

#Кидаю порт
EXPOSE 8080

#Not Root User
USER app

CMD ["/app/simple-app"]