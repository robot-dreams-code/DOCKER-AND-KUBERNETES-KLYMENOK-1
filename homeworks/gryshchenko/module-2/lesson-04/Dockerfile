#  Використовуємо офіційний легкий образ Python 3.12
FROM python:3.12-slim

# Робоча директорія всередині контейнера
WORKDIR /app

# Копіюємо файли залежностей
COPY apps/course-app/requirements.txt .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо увесь код застосунку
COPY apps/course-app/ .

# Відкриваємо порт
EXPOSE 8080

# Команда запуску FastAPI через uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
