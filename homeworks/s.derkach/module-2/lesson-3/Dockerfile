#для компіляції застосунку будемо використовувати образ golang який містить всі необхідні бібліотеки
FROM golang:1.23-alpine AS build

WORKDIR /simple-app

COPY go.* ./
COPY static ./
COPY templates ./
RUN go mod download

COPY . .

RUN CGO_ENABLED=0 GOOS=linux go build -o /simple-app

#для запуска будемо використовувати alpine, щоб отримати менший за розміром образ, 
#оскільки нам не потрібні всі бібліотеки GO які використовувались для компіляції застосунку
FROM alpine:latest

WORKDIR /simple-app

COPY --from=build /simple-app ./

EXPOSE 8080

RUN adduser -D simpleappuser
USER simpleappuser

CMD ["./simple-app"]