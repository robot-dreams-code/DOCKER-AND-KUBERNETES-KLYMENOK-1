
## вносимо зміни в dockerfile додаємо файл /tmp/healthy буде потрібно для readinessProbe

```bash
RUN mkdir -p /tmp && \
    touch /tmp/healthy
```
## збираємо зміни, далі в нашому деплойменті використовуємо image viktor1sss/course-app:lesson-08

```bash
docker buildx build --platform linux/amd64,linux/arm64  -t viktor1sss/course-app:lesson-08 -f Dockerfile  ../../../../apps/course-app --push
```

## Створення Namespace

створюємо namespace:
```bash
k apply -f namespace.yml
```

## Деплой ресурсів

Застосуємо всі конфігураційні файли (ConfigMap, Deployment, Service, Ingress, Middleware, Secret):
```bash
k apply -f .
```

Це створить:
- **ConfigMap**: `course-app-config` зі змінними середовища.
- **Secret**: `course-app-tls` з SSL сертифікатом.
- **Middleware**: `redirect-https` для редиректу на HTTPS.
- **Deployment**: `course-app-deployment` (10 реплік).
- **Service**: `course-app-svc` (ClusterIP).
- **Ingress**: `course-app-ingress` з налаштованим TLS та редиректом.
- **Deployment**: `redis-deployment` (1 реплік).
- **Service**: `redis-course-app-svc` (ClusterIP).

## Налаштування доступу (Ingress)

Оскільки ми використовуємо локальний кластер, потрібно додати запис у файл `/etc/hosts`, щоб домен `course-app.local` вказував на наш локальний Ingress контролер. 

перевіряємо на якій айпі адресі працює траефік
```bash
k get svc -A
NAMESPACE        NAME                   TYPE           CLUSTER-IP      EXTERNAL-IP    PORT(S)                      AGE
course-app-dev   course-app-svc         ClusterIP      10.43.25.204    <none>         8080/TCP                     4m47s
course-app-dev   redis-course-app-svc   ClusterIP      10.43.216.148   <none>         6379/TCP                     4m47s
default          kubernetes             ClusterIP      10.43.0.1       <none>         443/TCP                      29d
kube-system      kube-dns               ClusterIP      10.43.0.10      <none>         53/UDP,53/TCP,9153/TCP       29d
kube-system      metrics-server         ClusterIP      10.43.29.17     <none>         443/TCP                      29d
kube-system      traefik                LoadBalancer   10.43.67.37     192.168.64.2   80:32524/TCP,443:31205/TCP   29d
```
прописуємо в файл /etc/hosts
```
192.168.64.2 course-app.local
```

Тепер перевіряємо у браузері: [http://course-app.local](http://course-app.local)
повинен спрацювати редирект на [https://course-app.local](https://course-app.local)
```bash
curl -I http://course-app.local

HTTP/1.1 308 Permanent Redirect
Location: https://course-app.local/
Date: Sat, 29 Nov 2025 20:51:43 GMT
Content-Length: 18
```
## встановлюємо нейм спейс по дефолту
```bash
k config set-context --current --namespace=course-app-dev
```
## Симуляція збою Readiness Probe
ріденес проба `readinessProbe` налаштована на перевірку наявності файлу `/tmp/healthy`. Це дозволяє вручну зімітувати збій.

1. **Обираємо под**:
   ```bash
   k get pods

   NAME                                     READY   STATUS    RESTARTS      AGE
course-app-deployment-5849d77bd9-4h294   1/1     Running   2 (55s ago)   64s
course-app-deployment-5849d77bd9-fgblv   1/1     Running   2 (54s ago)   64s
course-app-deployment-5849d77bd9-mg44x   1/1     Running   2 (55s ago)   64s
course-app-deployment-5849d77bd9-mldj4   1/1     Running   2 (55s ago)   64s
course-app-deployment-5849d77bd9-rf4rn   1/1     Running   2 (54s ago)   64s
course-app-deployment-5849d77bd9-rfkzw   1/1     Running   2 (54s ago)   64s
course-app-deployment-5849d77bd9-t7lnn   1/1     Running   2 (54s ago)   64s
course-app-deployment-5849d77bd9-wq6v5   1/1     Running   2 (54s ago)   64s
course-app-deployment-5849d77bd9-x225n   1/1     Running   2 (54s ago)   64s
course-app-deployment-5849d77bd9-zlln2   1/1     Running   2 (54s ago)   64s
redis-deployment-856fd4bb8-qg5jm         1/1     Running   0             64s

   ```
2. ** перевіряємо endpoints**
   ```bash
   k get endpoints course-app-svc

NAME             ENDPOINTS                                                        AGE
course-app-svc   10.42.0.216:8080,10.42.0.217:8080,10.42.0.218:8080 + 7 more...   2m50s
   ```
3. **Видаляємо файл перевірки** (імітуємо збій):
   ```bash
   k exec course-app-deployment-5849d77bd9-rf4rn -- rm /tmp/healthy
   ```

4. **Перевіряємо статус**:
   Под перейде в статус `Running` (0/1 Ready).
   ```bash
   k get pods 

   NAME                                     READY   STATUS    RESTARTS        AGE
course-app-deployment-5849d77bd9-4h294   1/1     Running   2 (4m11s ago)   4m20s
course-app-deployment-5849d77bd9-fgblv   1/1     Running   2 (4m10s ago)   4m20s
course-app-deployment-5849d77bd9-mg44x   1/1     Running   2 (4m11s ago)   4m20s
course-app-deployment-5849d77bd9-mldj4   1/1     Running   2 (4m11s ago)   4m20s
course-app-deployment-5849d77bd9-rf4rn   0/1     Running   2 (4m10s ago)   4m20s
course-app-deployment-5849d77bd9-rfkzw   1/1     Running   2 (4m10s ago)   4m20s
course-app-deployment-5849d77bd9-t7lnn   1/1     Running   2 (4m10s ago)   4m20s
course-app-deployment-5849d77bd9-wq6v5   1/1     Running   2 (4m10s ago)   4m20s
course-app-deployment-5849d77bd9-x225n   1/1     Running   2 (4m10s ago)   4m20s
course-app-deployment-5849d77bd9-zlln2   1/1     Running   2 (4m10s ago)   4m20s
redis-deployment-856fd4bb8-qg5jm         1/1     Running   0               4m20s
   ```

5. **Перевіряємо Endpoints**:
   IP-адреса цього поду зникне зі списку ендпоінтів сервісу, і трафік на нього не йтиме, бачимо що стало на один меньше було 3+7 стало 3+6.
   ```bash
   k get endpoints course-app-svc 
   NAME             ENDPOINTS                                                        AGE
course-app-svc   10.42.0.216:8080,10.42.0.217:8080,10.42.0.218:8080 + 6 more...   4m54s
   ```

## Очищення ресурсів

Щоб видалити всі створені ресурси:
```bash
k delete -f namespace.yml
```