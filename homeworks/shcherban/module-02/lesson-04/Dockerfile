FROM python:3.14-alpine3.22
WORKDIR /app

COPY requirements.txt .

RUN python3 -m venv .venv
RUN source .venv/bin/activate
RUN pip install -r requirements.txt

COPY src/ ./src

EXPOSE 8080

RUN chown -R 405 /app
USER 405

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

