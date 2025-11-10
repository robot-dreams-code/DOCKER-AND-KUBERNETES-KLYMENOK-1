# ======= Build stage =======
FROM golang:1.25-alpine AS build
WORKDIR /src

# Копіюемо
COPY . .

# Збіраємо бінарник
RUN CGO_ENABLED=0 GOOS=linux go build -o lesson-03 main.go

# ======= Runtime stage =======
FROM alpine:3.22 AS runtime
WORKDIR /src

# Створюємо користувача not root
RUN adduser -D -u 1000 deploy

# Копіюємо тільки бінарник
COPY --from=build /src/lesson-03 ./lesson-03

# Встановлюємо власника і права
RUN chown deploy:deploy ./lesson-03 && chmod +x ./lesson-03

EXPOSE 8080

USER deploy

CMD ["./lesson-03"]
