FROM golang:1.23-alpine AS builder
WORKDIR /app

COPY apps/simple-app/go.mod apps/simple-app/go.sum ./
RUN go mod download

COPY apps/simple-app/ .

RUN CGO_ENABLED=0 GOOS=linux go build -o /app/main .

FROM alpine:latest

RUN addgroup -S appgroup && adduser -S appuser -G appgroup

WORKDIR /app

COPY --from=builder /app/main .
COPY --from=builder /app/templates ./templates
COPY --from=builder /app/static ./static

RUN chown -R appuser:appgroup /app

USER appuser

EXPOSE 8080

CMD ["./main"]

