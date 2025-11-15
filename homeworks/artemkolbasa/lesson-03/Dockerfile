FROM golang:1.23.3 AS builder
WORKDIR /src
COPY go.mod go.sum ./
RUN go mod download
COPY . .
RUN CGO_ENABLED=0 GOOS=linux GOARCH=amd64 go build -o simple-app ./

FROM scratch
WORKDIR /app
COPY --from=builder /src/simple-app /app/simple-app
USER 1000
EXPOSE 8080
ENTRYPOINT ["/app/simple-app"]