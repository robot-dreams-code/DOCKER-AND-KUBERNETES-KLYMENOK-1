FROM python:3.13.9-trixie AS builder 

ENV APP_HOME=/home/app
RUN mkdir -p $APP_HOME
WORKDIR $APP_HOME


COPY ./apps/course-app/ $APP_HOME
# Install Python deps
RUN python -m pip install --upgrade pip setuptools wheel \
    && pip install --no-cache-dir -r requirements.txt
# Ensure .env isn't used in image; env should be injected at runtime
ENV PYTHONUNBUFFERED=1


EXPOSE 8080
ENV PATH="/usr/local/bin:$PATH"
ENV APP_STORE=redis
ENV APP_DB_PATH=/data/app.db
ENV APP_REDIS_URL=redis://redis:6379/0
ENV APP_MESSAGE="Welcome to the Course Application!"

# Run your Python application
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]