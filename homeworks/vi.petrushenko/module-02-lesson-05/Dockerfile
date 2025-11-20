FROM python:3.12-slim
WORKDIR /app
COPY apps/course-app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY apps/course-app/src ./src
EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
