FROM python:3.11-alpine3.22

WORKDIR /app
COPY ./course-app/requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY ./course-app/src ./src

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
