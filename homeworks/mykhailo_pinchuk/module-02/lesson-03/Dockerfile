FROM golang:1.25-alpine AS build

WORKDIR /src

COPY apps/simple-app /src
RUN go mod download

RUN go build -o /bin/simple-app main.go

FROM alpine:latest

RUN adduser -D app
USER app

EXPOSE 8080

COPY --from=build /bin/simple-app /bin/simple-app

CMD ["/bin/simple-app"]
