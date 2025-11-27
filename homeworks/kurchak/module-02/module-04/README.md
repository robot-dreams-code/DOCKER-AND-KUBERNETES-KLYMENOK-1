# Course App

Нижче наведено мінімальні інструкції для локального запуску застосунку та перелік доступних змінних середовища

## Як запустити локально

### Варіант 1: Python (без Docker)
- Вимоги: Python 3.12+.
- Кроки
  1) Створити та активувати віртуальне середовище Python [W3Schools Instruction](https://www.w3schools.com/python/python_virtualenv.asp)
  2) Встановити залежності: `pip install -r requirements.txt`.
  3) Запустити застосунок: `uvicorn src.main:app --host 0.0.0.0 --port 8080`.
  4) Відкрити у браузері: http://localhost:8080

### Варіант 2: Dockerfile
Щоб запустити додаток з in-memory SQLite DB:
- Створити образ: `docker build -t course-app .`
- Створити та запустити контейнер: `docker run -p 8080:8080 course-app`

### Варіант 3: Docker Compose
Щоб запустити застосунок з Redis:
- Запуск: `docker compose up -d`
- Зупинка: `docker compose down`

## Змінні середовища

| Змінна | Опис | Приклад | Типове значення | Примітки |
|---|---|---|---|---|
| APP_MESSAGE | Текст повідомлення на головній сторінці | Hello | "Welcome to the Course App" |  |
| APP_STORE | Вибір бекенду сховища | sqlite | sqlite | Доступні: `sqlite`, `redis`. |
| APP_DB_PATH | Шлях до файлу SQLite | /data/app.db або data/data.sql | data/data.sql (локально)  | У контейнері можна використати `/data/app.db`. Локально за замовчуванням `data/data.sql`. |
| APP_REDIS_URL | URL підключення до Redis | redis://:password@host:6379/0 | redis://localhost:6379/0 | Використовується коли `APP_STORE=redis`. |
