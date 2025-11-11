# ---- deps stage --------------------------------------------------------------
ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim AS deps

WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --upgrade pip wheel && \
    pip wheel --wheel-dir=/wheels -r requirements.txt

# ---- runtime stage -----------------------------------------------------------
FROM python:${PYTHON_VERSION}-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PIP_NO_CACHE_DIR=1

RUN useradd --create-home --uid 10001 appuser
WORKDIR /app

COPY --from=deps /wheels /wheels
COPY requirements.txt .
RUN pip install --no-index --find-links=/wheels -r requirements.txt && rm -rf /wheels

COPY app ./app
COPY .env ./.env

EXPOSE 8080
USER appuser

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
