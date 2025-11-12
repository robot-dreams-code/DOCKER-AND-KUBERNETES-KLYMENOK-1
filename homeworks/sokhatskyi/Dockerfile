FROM golang:1.25.3-alpine AS build
WORKDIR /src

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o /bin/simple-app ./main.go

EXPOSE 8080

FROM alpine:3.22.2

RUN adduser -D app
USER app

COPY --from=build /bin/simple-app /bin/simple-app

CMD ["/bin/simple-app"]
