FROM golang:1.25.3-alpine3.22 AS build
WORKDIR /app

COPY ./apps/simple-app/go.mod ./apps/simple-app/go.sum ./
RUN go mod download

COPY ./apps/simple-app/ ./

RUN CGO_ENABLED=0 GOOS=linux go build -o /simple-app

FROM scratch
USER 1000
COPY --from=build /simple-app /simple-app
EXPOSE 8080

CMD ["/simple-app"]
