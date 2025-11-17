FROM python:3.12

EXPOSE 8080

WORKDIR app

ADD course-app /app

RUN apt-get update && apt-get install -y curl && pip install -r requirements.txt

HEALTHCHECK --interval=30s --timeout=3s CMD curl -f http://localhost:8080/health || exit 1

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
