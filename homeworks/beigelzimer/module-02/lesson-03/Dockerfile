FROM  golang:1.25.4 AS build
WORKDIR /apps/simple-app 

COPY go.mod go.sum ./
RUN go mod download

COPY  . .
RUN go build -o /app main.go


FROM debian:stable-20251103-slim

RUN useradd app
USER app

COPY --from=build /app /app

EXPOSE 8080
CMD ["/app"]