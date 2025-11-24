FROM python:3.13.9-trixie AS builder 

WORKDIR /app
# Install system dependencies
#RUN apt-get update \
#    && apt-get install -y --no-install-recommends gcc libpq-dev build-essential \
#    && rm -rf /var/lib/apt/lists/*

COPY ./apps/course-app/requirements.txt .
# Install Python deps
#RUN python -m pip install fastapi
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt
# Copy application code
COPY ./apps/course-app/ .
# Ensure .env isn't used in image; env should be injected at runtime
ENV PYTHONUNBUFFERED=1

EXPOSE 8080

# Define environment variables (optional)
ENV APP_STORE=redis
ENV APP_DB_PATH=/data/app.db
ENV APP_REDIS_URL=redis://redis:6379/0
ENV APP_MESSAGE="Welcome to the Course Application!"

# Run your Python application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "6379"]