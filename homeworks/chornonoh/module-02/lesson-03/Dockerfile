FROM golang:1.23 AS build

WORKDIR /simple-app

# Copy only dependency defs
COPY go.mod go.sum ./
# Download dependencies
RUN go mod download

# Copy the source code
COPY . .
# Build the application
RUN CGO_ENABLED=0 GOOS=linux go build -v -o /bin/simple-app ./main.go

FROM scratch

COPY --from=build /bin/simple-app /bin/simple-app

EXPOSE 8080

CMD ["/bin/simple-app"]
