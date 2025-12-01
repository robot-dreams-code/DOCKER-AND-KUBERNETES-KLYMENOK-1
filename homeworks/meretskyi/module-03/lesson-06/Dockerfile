FROM python:3.14.0-alpine3.21

WORKDIR /app
COPY . .

RUN ls -la

RUN python -m venv course-app \
    && pip install -r requirements.txt

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

EXPOSE 8080