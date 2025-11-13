FROM golang:1.25-alpine AS build

# Create nonroot user
RUN adduser -D simpleappuser
# Create workdir
WORKDIR /app

# Copy Go dependencies and download
COPY apps/simple-app/go.mod apps/simple-app/go.sum ./
RUN go mod download

# Copy app's files and compile app
COPY apps/simple-app ./
RUN CGO_ENABLED=0 GOOS=linux go build -o /simpleapp

FROM scratch

# Copy binary file and users from build stage
COPY --from=build /simpleapp /simpleapp
COPY --from=build /etc/passwd /etc/passwd

USER simpleappuser
EXPOSE 8080

ENTRYPOINT ["/simpleapp"]
