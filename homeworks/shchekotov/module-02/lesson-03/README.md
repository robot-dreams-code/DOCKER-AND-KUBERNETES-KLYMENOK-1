Створення та управління Docker образами
------------
### 1.1 Dockerfile для застосунку apps/simple-app

Збірка образу:

`docker build -t simple-app:latest -f homeworks/shchekotov/module-02/lesson-03/Dockerfile .`

Запуск контейнеру:

`docker rm simple-app; docker run --name simple-app -p 8080:8080 simple-app`

### 1.2 Властивості зібраних контейнерів

**Звичайна збірка:**

Для прямої збірки Disk Usage складає **1.34GB**, а Content Size **326MB**. Немало як для тестового застосунку.

**Multistage збірка:**

Для multistage отримуємо **17.1MB** Disk Usage i **6.12MB** Content Size.

**Multistage збірка, з ldflags:**

Можна ще зменшити розмір контейнера за рахунок додавання флагів на етапі компіляції.

`ARG LDFLAGS="-s -w"`

`RUN CGO_ENABLED=0 GOOS=linux go build -o app -ldflags "$LDFLAGS" .`


Флаг **-w** виключає зі збірки дані, що необхідні для дебагу збірки.
Флаг **-s** виключає зі збірки дані, про назви змінних, функцій, структур, тощо.  

Для такої збірки `docker images` показав  10.7MB і 3.17MB для Disk Usage та Content Size відповідно.

### 1.3 Перевірка користувача під яким запущено контейнер

Зазвичай користувача під яким запущено контейнер можна отримати 
за допомогою команди:

`docker exec simple-app whoami`

Для не multistage збірки без вказання користувача отримуємо `root`.


Для образів на основі scratch вищенаведений спосіб не працює, через відсутність оболонки командного рядка.

`docker inspect simple-app | grep User`.

Якщо поле User порожнє, або містить root, то контейнер запущено під суперкористувачем. 
У протилежному випадку контейнер запущено під вказаним коористувачем.

Після додавання у Dockerfile `USER 1000`, можна побачити що значення змінилось з `"User": ""` на `"User": "1000"`.

### 1.1 Публікація образу в репозиторій Docker Hub

Присвоюємо ім'я за принципом **username/image:latest**:

`docker tag simple-app 3floz/simple-app`

За потреби робимо логін:

`docker login`

Пушимо в репозиторій Docker Hub:

`docker push 3floz/simple-app`

Перевіряємо:

`docker run --name simple-app -p 8080:8080 3floz/simple-app`
