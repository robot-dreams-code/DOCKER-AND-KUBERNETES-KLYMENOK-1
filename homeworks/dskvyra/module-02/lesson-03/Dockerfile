# Stage 1: Build the Go app
FROM golang:1.24-alpine AS build

# Set working directory inside the container
WORKDIR /app

# Copy go.mod and go.sum files for dependency resolution
COPY go.mod go.sum ./

# Download dependencies
RUN go mod download

# Copy the rest of the source code
COPY . .

# Build the Go app binary
RUN go build -o app main.go

# Stage 2: Minimal runtime image
FROM alpine:latest

# Create non-root user and group
RUN addgroup -S appgroup && adduser -S appuser -G appgroup

# Set working directory
WORKDIR /app

# Copy the binary from build stage
COPY --from=build /app/app .

# Change ownership to the non-root user
RUN chown appuser:appgroup /app/app

# Switch to non-root user
USER appuser

# Expose port 8080
EXPOSE 8080

# Run the application
CMD ["./app"]