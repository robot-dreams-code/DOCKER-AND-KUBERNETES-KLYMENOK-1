FROM python:3.11-slim AS builder
WORKDIR /app
COPY ./requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
RUN useradd -m courseappuser
WORKDIR /app
COPY --from=builder /install /usr/local
COPY ./ .
RUN chown -R courseappuser:courseappuser /app
USER courseappuser
EXPOSE 8080
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
