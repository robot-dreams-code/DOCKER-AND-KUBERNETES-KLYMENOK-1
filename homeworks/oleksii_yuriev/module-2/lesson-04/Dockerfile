FROM python:3.14-alpine3.22

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN adduser -D -u 1000 appuser  \
    && chown -R appuser:appuser /app

EXPOSE 8080
USER appuser

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
