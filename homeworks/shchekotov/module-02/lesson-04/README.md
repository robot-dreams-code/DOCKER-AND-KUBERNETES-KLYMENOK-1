Docker Compose (частина 1)
------------
### 1.1 Dockerfile для застосунку apps/course-app

Перш за все треба встановити залежності для застосунку. 
Це можна зробити через `pip` використовуючи флаги `--no-cache-dir` і `--prefix`.
Перший вказує не створювати директорію з кешем залежностей, щоб не збільшувати розмір контейнера.
Другий дозволяє явно вказати директорію куди встановлювати залежності.

`RUN pip install --no-cache-dir --prefix=/deps -r requirements.txt`

У випадку із multistage збіркою спочатку переносимо залежності `COPY --from=builder /deps /usr/lib` а потім переносимо сам застосунок `COPY $APP_DIR/ .`

### 1.2 Налаштування середовища

Середовище можна налаштувати за допомогою `.env` файлу, додавши сюди всі необхідні змінні середовища.
Для генерації `REDIS_PASSWORD` та `APP_SECRET_TOKEN` я використовував команду `< /dev/urandom tr -dc a-zA-Z0-9 | head -c <кількість_символів>`.
В Docker Compose створений файл можна додати вказавши ім'я файлу у всередині властивості `env_file`.

### 1.3 Запуск застосунку

Запуск явно вказуючи docker-compose файл:

`docker compose -f homeworks/shchekotov/module-02/lesson-04/docker-compose.yaml up`

Зупинка:

`docker compose -f homeworks/shchekotov/module-02/lesson-04/docker-compose.yaml down`

Якщо в образ було внесено зміни то команду `down` можна виконати із флагом `--rmi local`. 
Це вказує видалити локальні образи, і при наступному запуску їх буде перезібрано. 