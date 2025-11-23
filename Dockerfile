FROM python:3.13-alpine

WORKDIR /course-app
COPY ./requirements.txt ./
RUN pip install -r requirements.txt 
COPY ./src/ .
ENV PATH=/usr/local/bin:/bin:/sbin:$PATH
RUN cd .
EXPOSE 8080
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
