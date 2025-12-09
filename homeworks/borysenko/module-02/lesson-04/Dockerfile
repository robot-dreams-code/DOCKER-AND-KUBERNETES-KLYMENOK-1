FROM python:3.12.12-trixie

WORKDIR /add


COPY ./apps/course-app/requirements.txt /add/

RUN pip install -r requirements.txt

COPY ./apps/course-app/src/main.py .
#Кидаю порт
EXPOSE 8080

#Not Root User
RUN useradd app

RUN mkdir /add/data
RUN chown -R app:app /add/data

USER app


CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]