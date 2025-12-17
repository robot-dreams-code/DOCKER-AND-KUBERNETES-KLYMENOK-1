============================================
     README — Lesson 11
============================================

Lesson 11 — Створення власного Helm-чарту для course-app
Module 03 / Lesson 11

Мета роботи:

Перенести створену в попередніх домашніх завданнях інфраструктуру (App + Redis + Ingress) з "сирих" маніфестів (kubectl apply) у керований Helm-чарт
Створення власного Helm-чарту для course-app
Створіть чарт для вашого застосунку, перенісши логіку з маніфестів попередніх занять (Deployment, Service, Ingress). Вимоги:
Шаблонізація: Основні параметри мають бути винесені у values.yaml (образ контейнера, тег, кількість реплік, хост Ingress)
Гнучкість: У шаблонах не повинно залишитись хардкоду, який заважав би розгорнути чарт у іншому неймспейсі чи з іншими налаштуваннями.
Розгортання Redis через Bitnami Redis Chart
Замість написання власного StatefulSet для Redis, розгорніть базу даних, використовуючи популярний ком'юніті-чарт bitnami/redis
Додайте відповідний репозиторій Helm
Встановіть Redis у ваш кластер, налаштувавши необхідні параметри


Передумови:
- Встановлено: kubectl, helm, docker
- Працює кластер Kubernetes (Rancher Desktop / Minikube / ін.)
- У кластері вже є встановлений Ingress-контролер (traefik / nginx)
- Є репозиторій образів: horodynskyiov/course-app:lesson-11


Namespace для уроку: lesson-11
Домен для Ingress: course-app.127.0.0.1.sslip.io


========================================
1. Підготовка Docker-образу course-app
========================================

1.1. Перейти в каталог з Dockerfile застосунку:

    cd C:\Robotdreams.CC\projects\lesson-11\app


1.2. Зібрати образ з тегом lesson-11:

    docker build -t horodynskyiov/course-app:lesson-11 .

1.3. Відправити образ у Docker Hub:

    docker push horodynskyiov/course-app:lesson-11


========================================
2. Налаштування Helm репозиторію Bitnami
========================================

2.1. Створити чарт:
     
    helm create course-app


2.2. Додати репозиторій Bitnami:

    helm repo add bitnami https://charts.bitnami.com/bitnami

2.3. Оновити індекс репозиторіїв:

    helm repo update


========================================
3. Створення namespace
========================================

3.1. Створити namespace lesson-11:

    kubectl create namespace lesson-11


========================================
4. Встановлення Redis через Bitnami Helm Chart
========================================

Release name: course-redis
Namespace: lesson-11
Архітектура: standalone
Пароль: вимкнено (auth.enabled=false)

4.1. Встановити Redis:

    helm install course-redis bitnami/redis --namespace lesson-11 --set architecture=standalone --set auth.enabled=false

4.2. Перевірити pod’и в namespace:

    kubectl get pods -n lesson-11

Вивод:

NAME                    READY   STATUS    RESTARTS   AGE
course-redis-master-0   1/1     Running   0          2m4s

4.3. Перевірити сервіси Redis:

    kubectl get svc -n lesson-11

Вивод:

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
course-redis-headless   ClusterIP   None            <none>        6379/TCP   2m46s
course-redis-master     ClusterIP   10.43.245.241   <none>        6379/TCP   2m46s

========================================
5. Підготовка Helm-чарту для course-app
========================================

Структура:

    C:\Robotdreams.CC\projects\lesson-11\course-app\
      Chart.yaml
      values.yaml
      templates\
        deployment.yaml
        service.yaml
        ingress.yaml
        _helpers.tpl

========================================
6. Розгортання Helm-чарту course-app
========================================

6.1. Перейти в каталог з Helm-чартом:

    cd C:\Robotdreams.CC\projects\lesson-11\course-app

6.2. Встановити / оновити чарт course-app у namespace lesson-11:

    helm upgrade --install course-app . -n lesson-11

(якщо потрібно явно задати тег, можна так:)

    helm upgrade --install course-app . -n lesson-11 --set image.repository=horodynskyiov/course-app --set image.tag=lesson-11

6.3. Перевірити pod’и:

    kubectl get pods -n lesson-11

Вивод:

NAME                          READY   STATUS    RESTARTS   AGE
course-app-544c7df5b9-7wklr   1/1     Running   0          116s
course-redis-master-0         1/1     Running   0          6m42s


6.4. Перевірити сервіси:

    kubectl get svc -n lesson-11

Вивод:

NAME                    TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
course-app-svc          NodePort    10.43.97.90     <none>        8080:30080/TCP   40s
course-redis-headless   ClusterIP   None            <none>        6379/TCP         5m26s
course-redis-master     ClusterIP   10.43.245.241   <none>        6379/TCP         5m26s

6.5. Перевірити Ingress:

    kubectl get ingress -n lesson-11

Вивод:

NAME                 CLASS     HOSTS                           ADDRESS         PORTS   AGE
course-app-ingress   traefik   course-app.127.0.0.1.sslip.io   192.168.127.2   80      2m39s



========================================
7. Перевірка роботи застосунку
========================================

7.1. Відкрити у браузері:

    http://course-app.127.0.0.1.sslip.io/

7.2. Переконатися, що:
- сторінка course-app відкривається;
- функціонал, який використовує Redis (сесії / лічильники / дані), працює.

За потреби переглянути логи застосунку:

    kubectl logs -n lesson-11 deployment/course-app
> course-app@1.0.0 start
> node index.js
Connected to Redis: redis://course-redis-master:6379
Server running on port 8080

    kubectl exec -it -n lesson-11 course-redis-master-0 -- redis-cli
127.0.0.1:6379> KEYS *
1) "visits"
127.0.0.1:6379> GET visits
"4"
127.0.0.1:6379>

========================================
8. Корисні команди для налагодження
========================================

8.1. Детальний опис pod’а course-app:

    kubectl describe pod -n lesson-11 <pod_name>

8.2. Перевірка підключення до Redis із pod’а course-redis-master:

    kubectl exec -it -n lesson-11 course-redis-master-0 -- redis-cli -h 127.0.0.1 -p 6379

8.3. Видалення релізів (для повного перепрозгортання):

    helm uninstall course-app -n lesson-11
    helm uninstall course-redis -n lesson-11

    kubectl delete namespace lesson-11
