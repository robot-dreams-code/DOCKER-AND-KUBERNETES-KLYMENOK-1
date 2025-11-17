# Simple Go Web App

This is a simple Go web application designed for Docker learning

## Dockerfile Overview

- Uses a multi-stage build to compile the Go binary in the first stage with the full Golang image
- The second stage copies only the compiled binary into a minimal Alpine image, significantly reducing the final image size
- Runs the application as a non-root user for security
- Exposes port `8080` for the web server

## .dockerignore

The `.dockerignore` excludes unnecessary files such as version control metadata, logs, and build outputs from the Docker build context to speed up builds and reduce image size.

## Building and Running

1. Build the Docker image (run this in the `apps/simple-app` directory):
```
docker build -t simple-app-image .
```

2. Run the container, mapping port 8080 from the container to your host:
```
docker run -p 8080:8080 simple-app-image
```

3. Access the app in your browser at: [http://localhost:8080](http://localhost:8080)

## How Multi-Stage Build Helps

Using a multi-stage Dockerfile keeps the final image small by separating build-time dependencies (like the Go compiler and source files) from the runtime image, which only contains the binary and necessary runtime environment. This improves build speed and makes the container more lightweight
