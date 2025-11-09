FROM python:3.14-slim-bookworm AS build
WORKDIR /app/

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.14-slim-bookworm AS runner
WORKDIR /app/
COPY --from=build /opt/venv /opt/venv

ENV PATH="/opt/venv/bin:$PATH"
COPY . /app/

EXPOSE 8080

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
