# ---- stage: builder ----
FROM python:3.12-slim AS builder
WORKDIR /src

COPY apps/course-app/requirements.txt ./
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---- stage: runtime ----
FROM python:3.12-slim

WORKDIR /src

RUN useradd -m appuser
USER appuser

COPY --from=builder /install /usr/local
COPY apps/course-app .

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]