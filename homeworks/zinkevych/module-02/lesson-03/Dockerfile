FROM golang:1.23 AS build
WORKDIR /app

COPY ./apps/simple-app/go.mod ./apps/simple-app/go.sum ./
RUN go mod download

COPY ./apps/simple-app/ .
# Build statically linked binary for Alpine (CGO_ENABLED=0 ensures no dynamic lib dependencies, GOOS=linux targets Linux)
RUN CGO_ENABLED=0 GOOS=linux go build -o app .

FROM alpine:3.22
# Creates disabled user (no password, no home)
RUN adduser -D appuser
COPY --from=build /app/app /app

USER appuser
EXPOSE 8080

ENTRYPOINT ["/app"]
