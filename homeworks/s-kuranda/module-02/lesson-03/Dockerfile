ARG GO_VERSION="1.23"

# Stage 1
FROM golang:${GO_VERSION}-alpine AS build

ARG GO_VERSION="1.23"

WORKDIR /app

RUN echo ":: Build App with Go Version: ${GO_VERSION}"

# Копіювання go.mod та go.sum для обробки залежностей
COPY go.mod go.sum ./
RUN go mod download

# Копіюємо код застосунку
COPY . .

# Збірка нашого застосунку
# CGO_ENABLED=0 вимикає CGO, створюючи статично зв'язаний бінарний файл
# -a збирає всі пакети, включаючи пакети стандартних бібліотек
# -installsuffix cgo_enabled_0 гарантує, що кеш збірки не буде повторно використано для збірок з вимкненим cgo
# -ldflags="-s -w" видаляє таблицю символів та налагоджувальну інформацію для меншого бінарного файлу
RUN CGO_ENABLED=0 GOOS=linux go build -a -installsuffix cgo_enabled_0 -ldflags="-s -w" -o simple-app .

# Stage 2
FROM alpine:latest

LABEL maintainer="Serhii Kuranda" \
      version="1.2.3" \
      project="Robot Dreams Sample App"

# Set the working directory
WORKDIR /app/

# Копіюємо нашу збірку застосунку з стейджу build
COPY --from=build /app/simple-app .

# Зазначаемо порт для публікації (в метаданих)
EXPOSE 8080

# Команда запуску нашого застосунку
CMD ["./simple-app"]