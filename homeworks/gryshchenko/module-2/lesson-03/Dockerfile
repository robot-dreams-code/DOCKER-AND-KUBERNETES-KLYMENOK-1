FROM golang:1.23-alpine AS build
WORKDIR /app
COPY go.mod go.sum ./
RUN go mod download
COPY . .

RUN go build -o simple-app .

FROM alpine:latest AS runtime
WORKDIR /app

COPY --from=build /app/simple-app .
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser
EXPOSE 8080

CMD ["./simple-app"]
