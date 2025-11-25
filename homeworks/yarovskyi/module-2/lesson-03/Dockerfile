FROM golang:1.25.4-alpine AS build-app

# create directory for the app code
WORKDIR /usr/local/app

# copy go.mod and go.sum files to install dependencies
COPY ./apps/simple-app/go.mod ./apps/simple-app/go.sum ./
RUN go mod download

# copy app code into the next separate layer
COPY ./apps/simple-app/ .

# build the app statically linked for linux OS
RUN CGO_ENABLED=0 GOOS=linux go build -o simple-app .

FROM alpine:3.22

# create non-root user
RUN adduser -D appuser
WORKDIR /app
USER appuser

# copy the binary from the build stage
COPY --from=build-app /usr/local/app/simple-app /app/simple-app

# expose port
EXPOSE 8080

# run the binary
ENTRYPOINT ["/app/simple-app"]
