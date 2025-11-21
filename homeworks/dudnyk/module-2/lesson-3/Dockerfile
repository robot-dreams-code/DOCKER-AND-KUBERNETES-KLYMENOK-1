FROM golang:1.25 AS builder

WORKDIR /app

COPY apps/simple-app/go.mod apps/simple-app/go.sum ./
RUN go mod download

COPY apps/simple-app/ ./

RUN CGO_ENABLED=0 GOOS=linux go build -o app main.go

FROM alpine:3.22

WORKDIR /app

COPY --from=builder /app/app /app

EXPOSE 8080

RUN adduser -D user
USER user

ENTRYPOINT ["./app"]

# запуск билда с корневой директории проекта
# docker build -t test1 -f ./homeworks/illia_dudnyk/module-2/lesson-3/Dockerfile .

# docker run -d --name simpleapp -p 8080:8080 test
