FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ../../../../apps/course-app/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ../../../../apps/course-app/src ./src/

RUN mkdir -p /app/data

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=3s --start-period=10s --retries=3 \
  CMD curl -fsS http://localhost:8080/healthz || exit 1

# Запускаємо застосунок
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
