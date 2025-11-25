FROM golang:1.23 AS build_app

WORKDIR /app

COPY ./apps/simple-app/ .

RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo -o main .

RUN groupadd -r app && useradd -r -g app app
RUN chown -R app:app /app

USER app

FROM alpine:latest

WORKDIR /app

COPY --from=build_app /app/main .

EXPOSE 8080

CMD ["./main"]