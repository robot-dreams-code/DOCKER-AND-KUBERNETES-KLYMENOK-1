FROM python:3.12-alpine

WORKDIR /app

COPY requirements.txt .

# Install dependencies directly into the image’s site-packages
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

WORKDIR /app

RUN adduser -D python
RUN chown -R python:python /app

USER python

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
