FROM golang:1.23 AS build

WORKDIR /app

COPY . .

WORKDIR /app/apps/simple-app
RUN go mod download

RUN CGO_ENABLED=0 go build -o /app/app

FROM alpine:3.20

WORKDIR /app
COPY --from=build /app/app .

EXPOSE 8080
USER nobody

ENTRYPOINT ["./app"]

