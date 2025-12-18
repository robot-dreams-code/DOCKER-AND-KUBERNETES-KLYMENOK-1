FROM golang:1.23-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux go build -o app main.go

FROM alpine:3.20 AS prod
WORKDIR /app
RUN adduser -D -g '' appuser
COPY --from=build /app/app .
RUN chown appuser:appuser /app/app
USER appuser
EXPOSE 8080
CMD ["/app/app"]
