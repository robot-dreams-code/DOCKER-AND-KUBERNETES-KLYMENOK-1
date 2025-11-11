FROM golang:1.23-alpine AS builder
WORKDIR /app
COPY apps/simple-app/go.mod apps/simple-app/go.sum ./
RUN go mod download
COPY apps/simple-app ./
RUN go build -o simple-app .

FROM alpine:latest
RUN addgroup -S simpleappgroup && adduser -S simpleappuser -G simpleappgroup
WORKDIR /app
COPY --from=builder /app/simple-app .
USER simpleappuser
EXPOSE 8080
CMD ["./simple-app"]
