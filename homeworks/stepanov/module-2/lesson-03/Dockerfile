FROM golang:1.23-alpine AS builder

WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .

RUN go build -o myapp .

FROM alpine:3.20

RUN adduser -D gouser

COPY --from=builder /app/myapp /usr/local/bin/myapp

USER gouser
EXPOSE 8080

CMD ["myapp"]
