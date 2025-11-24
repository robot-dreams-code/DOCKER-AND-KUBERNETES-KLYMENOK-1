# Stage 1: Build
FROM golang:1.23 AS builder
WORKDIR /app

ARG APP_DIR="apps/simple-app"
COPY $APP_DIR/go.mod $APP_DIR/go.sum ./
RUN go mod download

COPY $APP_DIR/ .

# Using ldflags to reduce binary size
ARG LDFLAGS="-s -w"
RUN CGO_ENABLED=0 GOOS=linux go build -o app -ldflags "$LDFLAGS" .

# Stage 2: Create runtime image
FROM scratch

USER 1000

COPY --from=builder /app .

EXPOSE 8080

ENTRYPOINT ["./app"]