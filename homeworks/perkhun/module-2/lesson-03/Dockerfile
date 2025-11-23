FROM golang:1.23-alpine as go-builder

WORKDIR /app

COPY apps/simple-app/go.mod apps/simple-app/go.sum ./

RUN go mod download

COPY apps/simple-app ./

RUN go build -o simple-app

FROM alpine:latest

RUN adduser -D appuser

WORKDIR /app

COPY --from=go-builder /app/simple-app .

EXPOSE 8080

USER appuser

CMD ["./simple-app"]



