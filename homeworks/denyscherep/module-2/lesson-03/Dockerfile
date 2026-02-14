FROM golang:1.23-alpine AS builder
RUN apk add --no-cache git ca-certificates && \
    addgroup -g 1000 appuser && \
    adduser -D -u 1000 -G appuser appuser
WORKDIR /build
COPY ../../../../apps/simple-app/go.mod go.sum ./
RUN go mod download
COPY ../../../../apps/simple-app .
RUN CGO_ENABLED=0 go build -ldflags="-w -s" -o app .

FROM scratch
COPY --from=builder /etc/ssl/certs/ca-certificates.crt /etc/ssl/certs/
COPY --from=builder /etc/passwd /etc/passwd
COPY --from=builder /etc/group /etc/group
COPY --from=builder /build/app /app
USER appuser
EXPOSE 8080
ENTRYPOINT ["/app"]