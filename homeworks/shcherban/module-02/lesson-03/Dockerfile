FROM golang:1.23 AS build
WORKDIR /app

COPY . .

RUN useradd -m app
USER app

RUN CGO_ENABLED=0 go build -o /home/app/app .

FROM scratch
COPY --from=build /home/app/app /bin/app

EXPOSE 8080

CMD ["/bin/app"]
