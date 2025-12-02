FROM python:3.14-slim
RUN apt-get update && apt-get install -y curl --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY ./apps/course-app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./apps/course-app/src .

RUN adduser appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
