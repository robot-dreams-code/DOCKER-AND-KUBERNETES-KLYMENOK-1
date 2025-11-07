FROM golang:1.23 AS build
WORKDIR /src/app

COPY . .

RUN useradd -m app
USER app

RUN CGO_ENABLED=0 GOOS=linux go build -o /home/app/app ./main.go

FROM alpine:3.22

USER 405

EXPOSE 8080

COPY --from=build /home/app/app /bin/app
CMD ["/bin/app"]
