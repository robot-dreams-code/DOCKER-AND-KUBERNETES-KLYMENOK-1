FROM golang:1.25.3 AS builder

WORKDIR /app

COPY . .

RUN go mod download && go build -o app main.go

FROM debian:bookworm-slim

WORKDIR /app

# Copy only the compiled binary and necessary assets
COPY --from=builder /app/app .
COPY --from=builder /app/static ./static
COPY --from=builder /app/templates ./templates

RUN useradd -m myappuser
USER myappuser

EXPOSE 8080

CMD ["./app"]