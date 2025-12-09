ARG CORP_REGISTRY=someregistry
FROM ${CORP_REGISTRY}/python:3.13-slim

ARG CORP_HOST=somename
ARG CORP_INDEX=somename
ARG CORP_INDEX_URL=somename

ENV CORP_HOST=${CORP_HOST}
ENV CORP_INDEX=${CORP_INDEX}
ENV CORP_INDEX_URL=${CORP_INDEX_URL}

WORKDIR /apps/couse-app 

COPY requirements.txt  ./

RUN pip install --cert=cert.crt --trusted-host="${CORP_HOST}" --index="${CORP_INDEX}" --index-url="${CORP_INDEX_URL}" -r requirements.txt

COPY  src ./src

EXPOSE 8080

RUN useradd  runapp
USER runapp

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]


