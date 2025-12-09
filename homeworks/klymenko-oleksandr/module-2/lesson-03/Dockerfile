FROM golang:1.23-alpine AS build
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o simple-app main.go

FROM alpine:3.20
WORKDIR /app
RUN adduser -D -u 10001 appuser
COPY --from=build /app/simple-app /app/templates /app/static ./
EXPOSE 8080
USER appuser
CMD ["./simple-app"]