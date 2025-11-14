# Multi-stage build strategy to reduce final image size:
# Stage 1: Install dependencies (may include build tools temporarily)
# Stage 2: Copy only installed packages, leaving build tools behind
# This reduces image size by ~17MB by excluding build artifacts and caches
FROM python:3.14-slim AS build
WORKDIR /app

# Create virtual environment
RUN python -m venv py-lesson-4
COPY ./apps/course-app/requirements.txt ./
# --no-cache-dir prevents pip from storing cache, reducing build stage size
RUN . py-lesson-4/bin/activate && pip install --no-cache-dir -r requirements.txt

# Final stage: Start fresh with minimal base image
FROM python:3.14-slim
WORKDIR /app

# Copy only the virtual environment (installed packages) from build stage
# Build tools, caches, and temporary files are left behind in build stage
COPY --from=build /app/py-lesson-4 ./py-lesson-4
COPY ./apps/course-app/src ./src

EXPOSE 8080

CMD ["./py-lesson-4/bin/uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
