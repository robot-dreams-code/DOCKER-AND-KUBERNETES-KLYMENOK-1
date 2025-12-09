FROM golang:1.23 AS builder
WORKDIR /app

COPY ./apps/simple-app/go.mod ./apps/simple-app/go.sum ./
RUN go mod download

COPY ./apps/simple-app/ ./

RUN CGO_ENABLED=0 GOOS=linux go build -o tinyserv ./

FROM alpine:3.22

EXPOSE 8080
RUN adduser -D tester
WORKDIR /home/tester/app
COPY --from=builder ./app .
USER tester

ENTRYPOINT ["/home/tester/app/tinyserv"]