FROM python:3.13-slim AS builder

WORKDIR /app

COPY apps/course-app/requirements.txt .


RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.13-slim

WORKDIR /app

COPY apps/course-app .
COPY --from=builder /usr/local /usr/local

RUN useradd -r -s /bin/false courseapp && \
    chown -R courseapp:courseapp /app

USER courseapp

EXPOSE 8080

# Use CMD to make the image reusable for running tests or other commands
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
