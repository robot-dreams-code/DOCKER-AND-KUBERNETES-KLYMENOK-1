FROM golang:1.23 AS build
WORKDIR /src
COPY ./apps/simple-app/go.mod ./apps/simple-app/go.sum .
RUN go mod download
ENV CGO_ENABLED=0
COPY ./apps/simple-app .
RUN go build -o /bin/simple-app ./main.go
EXPOSE 8080

FROM scratch
COPY --from=build /bin/simple-app /bin/simple-app
CMD ["/bin/simple-app"]
