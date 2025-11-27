FROM python:3.13-slim AS builder

COPY apps/course-app/requirements.txt .
RUN pip install -r requirements.txt

COPY apps/course-app .

FROM python:3.13-slim

WORKDIR /app

COPY apps/course-app .
COPY --from=builder /usr/local /usr/local

RUN useradd -r -s /bin/false courseapp && \
    chown -R courseapp:courseapp /app

USER courseapp

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "80"]