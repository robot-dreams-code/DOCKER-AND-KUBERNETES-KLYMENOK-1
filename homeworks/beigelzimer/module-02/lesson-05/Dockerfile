FROM python:3.13-slim
WORKDIR /apps/couse-app 

COPY requirements.txt  ./

RUN pip install -r requirements.txt
COPY  src ./src

RUN useradd runapp
USER runapp

EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]

