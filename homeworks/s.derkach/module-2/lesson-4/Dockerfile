FROM python:3.13-slim

COPY requirements.txt .
RUN pip install -r requirements.txt
WORKDIR /src
COPY src .
RUN useradd -m -u 1000 cappuser
USER cappuser
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]