FROM python:3.11-slim AS base

LABEL authors="dtimchuk"
LABEL module="module-2"
LABEL lesson="lesson-04"

WORKDIR /usr/src/app

# Install curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*

# copy requirements.txt for cache layer
COPY apps/course-app/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# delete .pyc files
ENV PYTHONDONTWRITEBYTECODE=1

# clear unnececery files
RUN find /usr/local -type d -name tests -exec rm -rf {} + && \
    find /usr/local -type d -name __pycache__ -exec rm -rf {} +

# copy rest files
COPY apps/course-app ./

# create dir for SQLite
RUN mkdir -p /data

# create user with home dir /home/app, with UUID 1000, change owner for directories /usr/src/app /data
RUN useradd -m -u 1000 app && chown -R app:app /usr/src/app /data
USER app

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]