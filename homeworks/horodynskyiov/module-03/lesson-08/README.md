# Course App – Домашнє завдання Kubernetes  
Module 03 / Lesson 08

Цей проєкт демонструє:

- Service Discovery через `Service` типу `ClusterIP`
- Перевірки стану (`livenessProbe`, `readinessProbe`)
- Зовнішню маршрутизацію через `Ingress`
- Забезпечення Zero Downtime при відмові pod'ів
- Збірку та локальний запуск Docker-образу
- Тестування готовності pod'ів через `.bat` скрипт

## Структура проєкту

lesson-08/
├─ Dockerfile
├─ index.js
├─ package.json
│
├─ deployment-service.yaml
├─ course-app-ingress.yaml
│
├─ zero-downtime-test.bat
│
└─ README.md


# Docker

## Збірка образу
docker build -t horodynskyiov/course-app:lesson-08 .

Запуск локально
docker run -p 8080:8080 horodynskyiov/course-app:lesson-08

Перевірка
http://localhost:8080
Hello from course-app:lesson-08

http://localhost:8080/health
Ok

************************************************
Kubernetes Deployment + Service

Файл: deployment-service.yaml

Цей manifest створює:

3 pod репліки

readinessProbe — очікує файл /tmp/healthy
livenessProbe — перевіряє /health
Service ClusterIP для Service Discovery

Застосувати:

kubectl apply -f deployment-service.yaml



***************************************************
Перевірка роботи Ingress

Після застосування Ingress можна швидко перевірити, що застосунок доступний зовні через домен.  
У цьому проєкті використовується домен формату `sslip.io`, який автоматично підставляє локальний IP (`127.0.0.1`).

### 1. Переконатися, що Ingress працює

kubectl get ingress
Очікуваний результат:
NAME                 CLASS     HOSTS                          ADDRESS   PORTS   AGE
course-app-ingress   traefik   course-app.127.0.0.1.sslip.io  127.0.0.1 80      10s

2. Перевірити, що Traefik піднятий
kubectl get pods -n kube-system

Має бути:
NAME                                      READY   STATUS      RESTARTS   AGE
coredns-6d668d687-dj4v5                   1/1     Running     1          56m
helm-install-traefik-2jws6                0/1     Completed   2          56m
helm-install-traefik-crd-c2shk            0/1     Completed   0          56m
local-path-provisioner-869c44bfbd-gkdqr   1/1     Running     1          56m
metrics-server-7bfffcd44-wdbd8            1/1     Running     1          56m
svclb-traefik-dbf9347c-mcfcm              2/2     Running     2          55m
traefik-865bd56545-qt6qf                  1/1     Running     1          55m


3. Перевірити стан сервісу та endpoint'ів

kubectl get svc course-app

NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
course-app   ClusterIP   10.43.184.146   <none>        8080/TCP   38m

kubectl get endpoints course-app
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME         ENDPOINTS                                         AGE
course-app   10.42.0.14:8080,10.42.0.15:8080,10.42.0.16:8080   39m

kubectl get pods -l app=course-app
NAME                          READY   STATUS    RESTARTS   AGE
course-app-78c4dcbfd5-4k6km   1/1     Running   0          39m
course-app-78c4dcbfd5-cwrvm   1/1     Running   0          39m
course-app-78c4dcbfd5-drztb   1/1     Running   0          39m


5. Перевірка в браузері

http://course-app.127.0.0.1.sslip.io
Очікуваний результат:
Hello from course-app:lesson-08

http://course-app.127.0.0.1.sslip.io/health
Очікуваний результат:
Ok

**************************************************
Ingress для роботи через HTTPS

Згенерувати самопідписаний сертифікат
openssl req -x509 -nodes -days 365 -newkey rsa:2048   -keyout course-app.key   -out course-app.crt   -subj "/CN=course-app.127.0.0.1.sslip.io/O=course-app"

Створити TLS secret у Kubernetes
kubectl create secret tls course-app-tls --cert=course-app.crt --key=course-app.key

Перевірити:
kubectl get secret course-app-tls

NAME             TYPE                DATA   AGE
course-app-tls   kubernetes.io/tls   2      5m40s

***Зміна конф *****
kubectl apply -f course-app-ingress.yaml

Перевірити, що Ingress з TLS
kubectl get ingress

NAME                 CLASS     HOSTS                           ADDRESS         PORTS     AGE
course-app-ingress   traefik   course-app.127.0.0.1.sslip.io   192.168.127.2   80, 443   56m

Перевірка в браузері

https://course-app.127.0.0.1.sslip.io
Очікуваний результат:
Hello from course-app:lesson-08

https://course-app.127.0.0.1.sslip.io/health
Очікуваний результат:
Ok


**************************************
Zero Downtime Test (.bat script)

Файл: zero-downtime-test.bat

Скрипт робить:

 позначає всі pod «готовими»
 обирає один pod
 переводить його в Not Ready
 перевіряє, що endpoint пропав
 відновлює
 показує результат



============================================ 
New run at: 25.11.2025 15:32:56,21 
============================================ 
 
[1/4] Making ALL course-app pods ready... 
  - readiness in pod: course-app-78c4dcbfd5-4k6km 
  - readiness in pod: course-app-78c4dcbfd5-cwrvm 
  - readiness in pod: course-app-78c4dcbfd5-drztb 
NAME                          READY   STATUS    RESTARTS   AGE
course-app-78c4dcbfd5-4k6km   1/1     Running   0          56m
course-app-78c4dcbfd5-cwrvm   1/1     Running   0          56m
course-app-78c4dcbfd5-drztb   1/1     Running   0          56m
[2/4] Selecting pod to simulate "Not Ready"... 
  Selected pod: course-app-78c4dcbfd5-4k6km 
[2.1] Breaking readiness in course-app-78c4dcbfd5-4k6km... 
Waiting 15 seconds... 
NAME                          READY   STATUS    RESTARTS   AGE
course-app-78c4dcbfd5-4k6km   0/1     Running   0          56m
course-app-78c4dcbfd5-cwrvm   1/1     Running   0          56m
course-app-78c4dcbfd5-drztb   1/1     Running   0          56m
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME         ENDPOINTS                         AGE
course-app   10.42.0.15:8080,10.42.0.16:8080   56m
[4/4] Restoring readiness in course-app-78c4dcbfd5-4k6km... 
Waiting 10 seconds... 
NAME                          READY   STATUS    RESTARTS   AGE
course-app-78c4dcbfd5-4k6km   1/1     Running   0          56m
course-app-78c4dcbfd5-cwrvm   1/1     Running   0          56m
course-app-78c4dcbfd5-drztb   1/1     Running   0          56m
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice
NAME         ENDPOINTS                                         AGE
course-app   10.42.0.14:8080,10.42.0.15:8080,10.42.0.16:8080   56m
--- END OF RUN --- 
