FROM python:3.14-slim

WORKDIR /app

COPY ./apps/course-app/requirements.txt .
RUN pip install -r requirements.txt

COPY ./apps/course-app/src .

RUN adduser appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
