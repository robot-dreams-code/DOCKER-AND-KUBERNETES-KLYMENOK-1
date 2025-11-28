# Building course-app image to push to Docker hub
# and to further deploy on k3c Rancher cluster 

FROM python:3.13.9-trixie AS builder
WORKDIR /app

# Install system dependencies
RUN apt-get update \
   && apt-get install -y --no-install-recommends gcc libpq-dev build-essential \
   && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .

# Install Python deps
RUN python -m pip install fastapi
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Ensure .env isn't used in image; env should be injected at runtime
ENV PYTHONUNBUFFERED=1
EXPOSE 8080

# Define environment variables (optional)
# Redis app is not included and should be deployed separately
ENV APP_STORE=redis
ENV APP_REDIS_URL=redis://redis:6379/0
ENV APP_MESSAGE="Welcome to the Course Application!"

# Run your Python application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]