# ======= Build stage =======
FROM golang:1.25-alpine AS build
WORKDIR /src

# Копируем исходники
COPY main.go .

# Сборка бина
RUN CGO_ENABLED=0 GOOS=linux go build -o course-app main.go

# ======= Runtime stage =======
FROM alpine:3.22 AS runtime
WORKDIR /app

# Создаем пользователя deploy
RUN adduser -D -u 1000 deploy

# Устанавливаем curl для healthcheck
RUN apk add --no-cache curl

# Копируем бинарник
COPY --from=build /src/course-app ./course-app

# Создаем папку для данных
RUN mkdir -p /app/data && chown -R deploy:deploy /app/data
RUN chown deploy:deploy ./course-app && chmod +x ./course-app

# Открываем порт приложения
EXPOSE 8080

# Переключаемся на пользователя deploy
USER deploy

# Команда запуска
CMD ["./course-app"]
