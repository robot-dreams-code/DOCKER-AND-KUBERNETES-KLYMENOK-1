# === STAGE 1: Builder ===
FROM golang:1.23-alpine AS builder

WORKDIR /app

# Копіюємо go.mod і go.sum
COPY apps/simple-app/go.* ./

# Завантажуємо залежності
RUN go mod download

# Копіюємо код
COPY apps/simple-app/ .

# Збираємо бінарник
RUN CGO_ENABLED=0 GOOS=linux go build -o main .

# === STAGE 2: Runtime ===
FROM alpine:latest

# Нерут-користувач
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -D -H appuser

WORKDIR /app

# Копіюємо тільки бінарник
COPY --from=builder --chown=appuser:appgroup /app/main .

USER appuser
EXPOSE 8080

CMD ["./main"]
