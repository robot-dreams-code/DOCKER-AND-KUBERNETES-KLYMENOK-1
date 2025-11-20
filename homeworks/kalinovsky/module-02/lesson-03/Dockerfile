# ---- stage: builder ----
FROM golang:1.23 AS builder
WORKDIR /src

COPY apps/simple-app/go.mod apps/simple-app/go.sum ./
run go mod download

COPY apps/simple-app ./
ENV CGO_ENABLED=0
RUN mkdir -p /app && go build -trimpath -o /app/simple-app ./...

EXPOSE 8080

# ---- stage: runtime ----
FROM alpine:3.18
RUN adduser -D appuser
USER appuser

COPY --from=builder /app/simple-app /app/simple-app

CMD ["/app/simple-app"]