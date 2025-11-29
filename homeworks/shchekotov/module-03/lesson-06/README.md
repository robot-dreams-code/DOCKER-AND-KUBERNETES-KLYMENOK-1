Основи Kubernetes
------------
### 1.1 Публічний образ для apps/course-app

Образ на основі застосунку apps/course-app доступний за посиланням [тут](https://hub.docker.com/r/3floz/course-app).

### 1.2 Конфігурування застосунку за допомогою .env файлів

Використовувати **.env** файли зручний спосіб для конфігурування застосунку. На відміну від Docker Compose де досить додати
властивість `env_file:` у `docker-compose.yaml`, **Kubernetes** через свою розподілену природу не надає подібного способу це зробити.
Як і більшість взаємодій із **Kubernetes** кластером, додати конфігурацію з .env файлів можна через **kubectl**.

`kubectl create configmap course-app-config --from-env-file=homeworks/shchekotov/module-03/lesson-06/env/course-app.env`

`kubectl create secret generic course-app-secret --from-env-file=homeworks/shchekotov/module-03/lesson-06/env/course-app-secret.env`

В роботі я використовував `namespace: default`, за потреби до вищенаведених команд можна додати флаг `-n` і явно вказати namespace.
Перевірити встановлені значення можна за допомогою **Rancher Cluster Dashboard** або **Kubectl**:

`kubectl get configmap course-app-config -o yaml`

`kubectl get secret course-app-secret -o yaml`

Флаг -o може приймати не лише yaml, але і інші формати, наприклад json.

### 1.3 Маніфест Deployment, Service для застосунку apps/course-app

Спочатку я спробував розбивати маніфест на кілька yaml файлів `(course-app.yaml, course-app-store.yaml, etc)`.
Однак з часом мені здалося зручнішим описувати все одним файлом `(deployment.yaml)`, розміщуючи деплойменти разом із сервісами. 

Команда запуску кластеру:

`kubectl apply -f homeworks/shchekotov/module-03/lesson-06/deployment.yaml`

### 1.4 Редеплой Кластеру

Для прикладу змінимо кількость реплік для `course-app` (наприклад з 1 до 7) у .yaml файлі, потім знов `kubectl apply -f ...`. 
Тоді щоб побачити прогресс редеплою виконуємо `kubectl rollout status deployment/course-app`, в результаті отримуємо наступний вивід:

> Waiting for deployment "course-app" rollout to finish: 1 of 7 updated replicas are available...  
> Waiting for deployment "course-app" rollout to finish: 2 of 7 updated replicas are available...  
> Waiting for deployment "course-app" rollout to finish: 3 of 7 updated replicas are available...  
> Waiting for deployment "course-app" rollout to finish: 4 of 7 updated replicas are available...  
> Waiting for deployment "course-app" rollout to finish: 5 of 7 updated replicas are available...  
> Waiting for deployment "course-app" rollout to finish: 6 of 7 updated replicas are available...  