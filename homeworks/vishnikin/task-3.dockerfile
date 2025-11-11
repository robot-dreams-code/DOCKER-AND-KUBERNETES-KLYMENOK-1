FROM python:3.11-slim

WORKDIR /apps/first-app

COPY ../../apps/course-app/requirements.txt ./
RUN pip install -r requirements.txt  

COPY ../../apps/course-app/src ./src
EXPOSE 8080

RUN useradd appuser
USER appuser

CMD ["python", "src/main.py", "--host", "0.0.0.0", "--port", "8080"]



 