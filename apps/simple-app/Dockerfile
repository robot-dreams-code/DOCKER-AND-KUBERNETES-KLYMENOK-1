FROM golang:alpine AS build
WORKDIR /app

COPY go.mod go.sum ./
RUN go mod download

COPY . .
RUN go build -o app main.go

FROM scratch
COPY --from=build --chown=1000:1000 /app/app /app
USER 1000
EXPOSE 8080
ENTRYPOINT ["/app"]

