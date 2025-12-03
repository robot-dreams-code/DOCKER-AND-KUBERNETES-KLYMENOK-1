============================================
     README — Lesson 10
============================================

Lesson 10 — Kubernetes StatefulSet + Redis + Course App
Module 03 / Lesson 10

Мета роботи:

Розгорнути Redis у Kubernetes за допомогою StatefulSet
Налаштувати PVC для зберігання даних Redis
Розгорнути Node.js застосунок course-app
Забезпечити інтеграцію з Redis (запис лічильника visits)
Виконати перевірку роботи


### 1. Перевірка StorageClass:
Команда:
cmd: kubectl get sc
NAME                   PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  8m49s

Очікуваний результат:
local-path (default)


### 2. Redis StatefulSet (k8s/redis-statefulset.yaml):
Застосовуння

cmd: kubectl apply -f k8s/redis-statefulset.yaml
statefulset.apps/redis created


Перевірка

cmd: kubectl get pods -l app=redis
NAME      READY   STATUS    RESTARTS   AGE
redis-0   1/1     Running   0          28s

cmd: kubectl get pvc
NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data-redis-0   Bound    pvc-e292b077-d8f2-4f26-9aa4-59039920bcc2   1Gi        RWO            local-path     <unset>                 59s


### 3. Redis Service (k8s/redis-service.yaml):

Застосовуння
cmd: kubectl apply -f k8s/redis-service.yaml
service/redis created

Перевірка

cmd: kubectl get svc redis
AME    TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
redis   ClusterIP   10.43.251.68   <none>        6379/TCP   10s


### 4. Course App — Deployment (course-app/course-app-deployment.yaml):

Створення:
cmd: kubectl apply -f course-app/course-app-deployment.yaml
deployment.apps/course-app created


### 5. Dockerfile та створення Docker-образу:

Збірка образу:
cmd: docker build -t horodynskyiov/course-app:lesson-10 .

Публікація:
cmd: docker push horodynskyiov/course-app:lesson-10

### 6. Перевірка роботи додатку:

cmd: kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
course-app-6b799ff477-nj42q   1/1     Running   0          78s
redis-0                       1/1     Running   0          6m27s

cmd: kubectl get svc
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
kubernetes   ClusterIP   10.43.0.1      <none>        443/TCP    8m10s
redis        ClusterIP   10.43.251.68   <none>        6379/TCP   5m28s

cmd: ubectl get pvc
NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data-redis-0   Bound    pvc-e292b077-d8f2-4f26-9aa4-59039920bcc2   1Gi        RWO            local-path     <unset>                 7m46s

Логи застосунку:
cmd: ubectl logs -l app=course-app

> course-app@1.0.0 start
> node index.js

Server running on port 8080

### 7. Перевірка роботи Redis:
cmd: kubectl exec -it redis-0 -- redis-cli
127.0.0.1:6379> KEYS *
1) "visits"
127.0.0.1:6379> GET visits
"7"
127.0.0.1:6379>


### 8. Доступ через браузер

Через NodePort:
http://127.0.0.1:30080/

Через Ingress (якщо створений):
http://course-app.127.0.0.1.sslip.io/


