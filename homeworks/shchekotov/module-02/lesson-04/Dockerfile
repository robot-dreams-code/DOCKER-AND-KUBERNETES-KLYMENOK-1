FROM python:3.14-slim AS builder
WORKDIR /app

ARG APP_DIR="apps/course-app"

COPY $APP_DIR/requirements.txt ./
RUN pip install --no-cache-dir --prefix=/deps -r requirements.txt

FROM python:3.14-slim
WORKDIR /app

RUN apt-get update && apt-get install -y curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

USER 1000
ARG APP_DIR="apps/course-app"

COPY --from=builder /deps /usr/local
COPY $APP_DIR/ .

EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]