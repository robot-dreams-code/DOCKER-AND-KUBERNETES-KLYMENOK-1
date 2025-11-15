FROM golang:1.23.0 AS builder
WORKDIR /app
COPY ./apps/simple-app/go.mod ./apps/simple-app/go.sum ./
RUN go mod download && go mod verify
COPY ./apps/simple-app ./
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o go-app .

FROM alpine:3.14
WORKDIR /app
RUN adduser -D appuser
COPY --from=builder /app/go-app .

USER appuser
EXPOSE 8080

ENTRYPOINT ["/app/go-app"]


