FROM golang:1.23-bookworm AS build

WORKDIR /app

COPY go.mod go.sum .
RUN go mod tidy

COPY . .

RUN CGO_ENABLED=0 go build -o app main.go

FROM scratch
COPY --from=build app .
USER 1000:1000
EXPOSE 8080

CMD ["./app"]