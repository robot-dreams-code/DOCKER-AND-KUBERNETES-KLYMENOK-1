ARG ENV_VERSION=3.14

FROM python:$ENV_VERSION-alpine3.22

LABEL maintainer="Serhii Kuranda" \
      version="2025.11.06" \
      project="Robot Dreams :: Lesson 04"

RUN apk update && \
    apk add curl jq bash && \
    rm -rf /var/cache/apk/*

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN adduser --disabled-password appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
