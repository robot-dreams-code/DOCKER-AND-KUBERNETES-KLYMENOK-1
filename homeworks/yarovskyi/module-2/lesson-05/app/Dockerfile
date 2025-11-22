FROM python:3.14.0

# create directory for the app code
WORKDIR /usr/local/app

# copy requirements.txt to install dependencies
COPY ./apps/course-app/requirements.txt .
RUN pip install -r requirements.txt

# copy app code into the next separate layer
COPY ./apps/course-app/ .

# create non-root user
RUN adduser --disabled-password --gecos "" appuser
RUN chown -R appuser:appuser /usr/local/app
USER appuser

# expose port
EXPOSE 8080

# run the binary
ENTRYPOINT ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
