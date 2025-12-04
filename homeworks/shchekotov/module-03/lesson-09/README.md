Робота з Persistent Storage у Kubernetes
------------
### 1.1 Публічний образ для apps/course-app

Результат виконання `kubectl get sc`:

> local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  17d 

### 2. Redis як StatefulSet (Основне завдання)

На цей раз в `deployment.yaml` лишаю лише `Service` та `Deployment` для `course-app`. 
Шар даних буде оголошено як `StatefulSet` в `redis-statefulset.yaml`. 
Вказую запускати одну репліку, змінюю таг образу на redis:7-alpine, PVC шаблон, розмір тому, 
режим доступу, тощо, вказані як в завданні.

### 3. Redis Service

Доступ до шару даних визначаю за допомогою `Service` в окремому файлі `redis-service.yaml`. 
Оголошую його як headless вказуючи `clusterIP: None` kube-proxy не буде здійснювати для цього сервісу віртуальну адресацію
всі запити будуть спрямовані напряму до подів з селектором `redis-statefulset`. Змінюємо ім'я сервісу в `config.kubernetes.io/depends-on` на `"[Service/redis]"`.

### 4. Оновлення Deployment course-app

У файлі .env/course-app.env змінюю значення змінної `APP_REDIS_URL` з `redis://course-app-store:6379/0` на `redis://redis:6379`.

Деплоїмо застосунок командою:
`kubectl apply -f homeworks/shchekotov/module-03/lesson-09/deployment.yaml \  
&& kubectl apply -f homeworks/shchekotov/module-03/lesson-09/redis-statefulset.yaml \  
&& kubectl apply -f homeworks/shchekotov/module-03/lesson-09/redis-service.yaml
`

Після успішного деплойменту перевіряємо чи працює персистентність. 
Переходимо за адресою `http://0.0.0.0:/30080` вносимо зміни в застосунку. Зупиняємо застосунок:

`kubectl delete -f homeworks/shchekotov/module-03/lesson-09/deployment.yaml \  
&& kubectl delete -f homeworks/shchekotov/module-03/lesson-09/redis-statefulset.yaml \  
&& kubectl delete -f homeworks/shchekotov/module-03/lesson-09/redis-service.yaml
`

Після повторного деплою бачимо внесені зміни, отже застосунок коректно працює з Persistent Storage. 