# Multi-stage build strategy to reduce final image size:
# Stage 1: Install dependencies
# Stage 2: Copy only installed packages, leaving build tools behind
FROM python:3.14-slim AS build
WORKDIR /app

COPY ./apps/course-app/requirements.txt ./
# Install dependencies to a custom location for easy copying
RUN pip install --no-cache-dir --target /app/deps -r requirements.txt

# Final stage: Start fresh with minimal base image
FROM python:3.14-slim
WORKDIR /app

# Install curl for healthchecks
RUN apt-get update && apt-get install -y --no-install-recommends curl && \
    rm -rf /var/lib/apt/lists/*

# Copy installed packages from build stage
COPY --from=build /app/deps /usr/local/lib/python3.14/site-packages
COPY ./apps/course-app/src ./src

EXPOSE 8080

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
