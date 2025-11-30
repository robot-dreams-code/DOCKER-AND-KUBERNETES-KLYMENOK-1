# robot_dreams :: Lessons-03

## Overview

This homework contains the Docker configuration and Makefile for building, running, and managing the **Robot Dreams Sample App**—a Go-based application. The setup is designed for easy local development and testing using Docker.

Key features:
- Builds a Docker image from a Go project located outside the main directory.
- Uses environment variables from `.env` for configuration.
- Provides Makefile targets for common workflows like building, starting, and stopping the container.

**Note on Project Structure**: The actual Go source code for the app resides in an external directory (`../../../../apps/simple-app` relative to this repo). This is handled via the `GO_PATH` variable in `.env`, allowing you to build the image without relocating the source code.

## Prerequisites

- Docker installed and running on your machine.
- Make (GNU Make) installed.
- Access to the external Go project directory (relative path: `../../../../apps/simple-app` from the root of this repo).

## Installation

1. Clone this repository (or navigate to the directory containing the `Dockerfile`, `Makefile`, and `.env`).

2. Copy the provided `.env` file to the root of this directory (or create your own with the required variables—see [Configuration](#configuration) below).

3. Ensure the Go project path in `GO_PATH` points correctly to your external source code directory. Adjust if your structure differs.

4. Run `make help` to verify the setup and see available commands.

## Configuration

The `.env` file drives the build and runtime settings. Here's the default structure:
- `GO_VERSION`: Go version used in the Docker build (passed as `--build-arg`).
- `GO_PATH`: Relative path to the external Go project directory. **Important**: This points outside the repo (e.g., `../../../../apps/simple-app`). Ensure this path is correct from the location of the `Dockerfile`.
- `IMAGE_NAME`: Name of the Docker image.
- `IMAGE_TAG`: Tag for the image (e.g., version or build identifier).
- `APP_NAME`: Name of the running container.
- `APP_EXT_PORT`: Host port to map to the container's internal port 8080 (e.g., access the app at `http://localhost:8082`).

Modify these as needed for your environment, but avoid committing sensitive values.

## Usage

All interactions are handled via the Makefile. Run `make help` for a formatted list of commands.

### Building the Image

- **Build with cache** (recommended for faster builds):
```
make build
```

This runs `docker build` using the `GO_PATH` and `GO_VERSION`.

- **Build without cache** (for clean rebuilds):
```
make build-no-cached
```

### Running the App

- **Start the container**:
```
make start
```

Launches the app in detached mode, mapping `localhost:${APP_EXT_PORT}` to the container's port 8080.

- **Stop the container**:
```
make stop
```

- **Restart the container**:
```
make restart
```

### Example Workflow

1. Build the image: `make build`
2. Start the app: `make start`
3. Test the app: Open `http://localhost:8082` in your browser.
4. Stop when done: `make stop`

## Troubleshooting

- **Path Issues**: If the build fails with "no such file or directory," double-check `GO_PATH`. Run `ls $(GO_PATH)` from the lesson root to verify.
- **Port Conflicts**: Change `APP_EXT_PORT` in `.env` if 8082 is in use.
- **Docker Not Found**: Ensure Docker is installed and the daemon is running (`docker --version`).
- **Go Version Mismatch**: Update `GO_VERSION` to match your project's requirements.

---

*Built with ❤️ for robot_dreams coach.*