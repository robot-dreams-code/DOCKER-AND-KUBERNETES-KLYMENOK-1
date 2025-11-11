# I used the official Golang image as the base image, took it from https://hub.docker.com/_/golang
FROM golang:1.23 AS stage-build

# Maintainer information
LABEL authors="dtimchuk"
# Metadata labels
LABEL module="module-2"
LABEL lesson="lesson-03"

# Set the working directory inside the container
WORKDIR /usr/src/app

# Due to I run this Dockerfile from the root of the repository,
# I need to copy the application code into the container
# docker build -f homeworks/dtimchuk/module-2/lesson-03/Dockerfile -t simple-app .
# where -f is used to specify the path to the Dockerfile
COPY apps/simple-app ./

# Download Go dependencies
RUN go mod download

# CGO_ENABLED=0 is used to build a statically linked binary, to execute C code from Go code
# This is important for running the binary in a minimal base image like scratch
RUN CGO_ENABLED=0 go build -o /usr/local/bin/app ./main.go
# Due to in scratch image there is no /etc/passwd file,
# we need to create a minimal one to run the application as non-root user (>=1000 === regular users),
# login is forbiden with "*"
RUN echo "app:*:1000:1000::/home/app:/bin/sh" > /tmp/passwd

# Use a minimal base image for the final stage
FROM scratch
# Copy the passwd file to allow non-root user execution
COPY --from=stage-build /tmp/passwd /etc/passwd
COPY --from=stage-build /usr/local/bin/app /usr/local/bin/app
# Switch to non-root user for better security -> set the user to 'app'
USER app

# Expose port 8080 to allow communication to/from the container
EXPOSE 8080
# Command to run the application with the specified port 8080
CMD ["app", "-port", "8080"]