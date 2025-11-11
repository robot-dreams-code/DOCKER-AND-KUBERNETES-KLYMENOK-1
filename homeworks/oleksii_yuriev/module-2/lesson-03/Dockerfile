FROM golang:1.25-alpine AS build
WORKDIR /app

COPY . .
RUN go build -o simple-app main.go

FROM alpine:3.22
WORKDIR /app
RUN adduser -D -u 1000 appuser
COPY --from=build /app/simple-app ./

EXPOSE 8080
USER appuser
CMD ["./simple-app"]
