FROM python:3.12-alpine

WORKDIR /app

COPY apps/course-app/requirements.txt ./
RUN pip install -r requirements.txt

COPY apps/course-app ./

RUN adduser -D user
RUN chown -R user:user /app
USER user

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]