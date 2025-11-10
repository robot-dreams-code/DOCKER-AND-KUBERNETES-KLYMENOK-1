FROM python:3.14.0-alpine3.22

EXPOSE 8080

WORKDIR /app

RUN addgroup -S deploy && adduser -S deploy -G deploy

RUN mkdir /data && chown deploy:deploy /data

RUN --mount=type=bind,source=requirements.txt,target=/app/requirements.txt,readonly pip install -r /app/requirements.txt

COPY --chown=deploy:deploy . /app/

USER deploy

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080" ]
