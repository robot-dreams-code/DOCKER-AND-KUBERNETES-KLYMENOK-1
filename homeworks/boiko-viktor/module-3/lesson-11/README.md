# Helm 

### Додавання Bitnami репозиторію

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Встановлення чарту

```bash
helm install course-app . -n course-app-dev --create-namespace

NAME: course-app
LAST DEPLOYED: Tue Dec  9 23:38:03 2025
NAMESPACE: course-app-dev
STATUS: deployed
REVISION: 1
TEST SUITE: None
```

# Перевірка подів
```bash
k get pods -n course-app-dev

NAME                          READY   STATUS    RESTARTS        AGE
course-app-84c9558999-67rlr   1/1     Running   3 (118s ago)    3m19s
course-app-84c9558999-6zphk   1/1     Running   3 (2m52s ago)   3m19s
course-app-84c9558999-8tx9d   1/1     Running   3 (2m54s ago)   3m19s
course-app-84c9558999-8vzkx   1/1     Running   3 (2m54s ago)   3m19s
course-app-84c9558999-dz7t6   1/1     Running   3 (118s ago)    3m19s
course-app-84c9558999-g2xnc   1/1     Running   3 (2m52s ago)   3m19s
course-app-84c9558999-gjj99   1/1     Running   3 (2m54s ago)   3m19s
course-app-84c9558999-grfg8   1/1     Running   2 (3m10s ago)   3m19s
course-app-84c9558999-hkk7p   1/1     Running   3 (2m28s ago)   3m19s
course-app-84c9558999-xg24h   1/1     Running   2 (3m10s ago)   3m19s
course-app-redis-master-0     1/1     Running   0               3m19s
```
# Перевірка всіх ресурсів

```bash
k get all -n course-app-dev
NAME                              READY   STATUS    RESTARTS        AGE
pod/course-app-84c9558999-67rlr   1/1     Running   3 (2m26s ago)   3m47s
pod/course-app-84c9558999-6zphk   1/1     Running   3 (3m20s ago)   3m47s
pod/course-app-84c9558999-8tx9d   1/1     Running   3 (3m22s ago)   3m47s
pod/course-app-84c9558999-8vzkx   1/1     Running   3 (3m22s ago)   3m47s
pod/course-app-84c9558999-dz7t6   1/1     Running   3 (2m26s ago)   3m47s
pod/course-app-84c9558999-g2xnc   1/1     Running   3 (3m20s ago)   3m47s
pod/course-app-84c9558999-gjj99   1/1     Running   3 (3m22s ago)   3m47s
pod/course-app-84c9558999-grfg8   1/1     Running   2 (3m38s ago)   3m47s
pod/course-app-84c9558999-hkk7p   1/1     Running   3 (2m56s ago)   3m47s
pod/course-app-84c9558999-xg24h   1/1     Running   2 (3m38s ago)   3m47s
pod/course-app-redis-master-0     1/1     Running   0               3m47s

NAME                                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/course-app                  ClusterIP   10.43.190.225   <none>        8080/TCP   3m47s
service/course-app-redis-headless   ClusterIP   None            <none>        6379/TCP   3m47s
service/course-app-redis-master     ClusterIP   10.43.16.33     <none>        6379/TCP   3m47s

NAME                         READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/course-app   10/10   10           10          3m47s

NAME                                    DESIRED   CURRENT   READY   AGE
replicaset.apps/course-app-84c9558999   10        10        10      3m47s

NAME                                       READY   AGE
statefulset.apps/course-app-redis-master   1/1     3m47s
```

### Перевизначення значень при встановленні

```bash
# Змінити кількість реплік
helm install course-app . -n course-app-dev \
  --set app.replicaCount=5

# Вимкнути TLS
helm install course-app . -n course-app-dev \
  --set ingress.tls.enabled=false

# Використати власний values файл
helm install course-app . -n course-app-dev \
  -f custom-values.yaml
```

### Робота з Redis

#### Підключення до Redis CLI

```bash
k exec -it -n course-app-dev course-app-redis-master-0 -- redis-cli
```

### Перевірка даних

```bash
# В Redis CLI
127.0.0.1:6379> KEYS *
1) "counters:visits"
127.0.0.1:6379> GET counters:visits
"0"
127.0.0.1:6379> GET counters:visits
"5"
127.0.0.1:6379>

```

### Оновлення чарту

```bash
# Оновити з новими параметрами
helm upgrade course-app . -n course-app-dev

# Оновити з конкретними значеннями
helm upgrade course-app . -n course-app-dev \
  --set app.image.tag=lesson-07 \
  --set app.replicaCount=15
```

### Історія релізів

```bash
# Переглянути історію
helm history course-app -n course-app-dev

# Відкотитися до попередньої версії
helm rollback course-app -n course-app-dev

# Відкотитися до конкретної ревізії
helm rollback course-app 1 -n course-app-dev
```

### Масштабування

```bash
# Горизонтальне масштабування застосунку
helm upgrade course-app . -n course-app-dev \
  --set app.replicaCount=20

# Вертикальне масштабування Redis
helm upgrade course-app . -n course-app-dev \
  --set redis.master.resources.limits.memory=1Gi \
  --set redis.master.resources.limits.cpu=1
```

### Видалення релізу (зберігає namespace)

```bash
helm uninstall course-app -n course-app-dev
```

### Повне видалення (включно з namespace)

```bash
helm uninstall course-app -n course-app-dev
k delete namespace course-app-dev
```

```bash
# Helm автоматично не видаляє PVC
k delete pvc -n course-app-dev -l app.kubernetes.io/name=redis
```

### Поди не запускаються

```bash
# Перевірити події
k get events -n course-app-dev --sort-by=.metadata.creationTimestamp

# Детальна інформація про под
kubectl describe pod -n course-app-dev <pod-name>

# Перевірити логи
kubectl logs -n course-app-dev <pod-name>
```

### Redis не підключається

```bash
# Перевірити, чи запущений Redis
k get pods -n course-app-dev -l app.kubernetes.io/name=redis

# Перевірити сервіс Redis
k get svc -n course-app-dev | grep redis

# Перевірити з'єднання з поду застосунку
k exec -it -n course-app-dev <app-pod> -- nc -zv course-app-redis-master 6379
```

### Ingress не працює

```bash
# Перевірити Ingress ресурс
k describe ingress -n course-app-dev

# Перевірити middleware
k get middleware -n course-app-dev


### Перевірка Helm релізу

```bash
# Інформація про реліз
helm get values course-app -n course-app-dev

USER-SUPPLIED VALUES:
redis:
  master:
    resources:
      limits:
        cpu: 1
        memory: 1Gi
# Згенеровані маніфести
helm get manifest course-app -n course-app-dev

# Всі деталі
helm get all course-app -n course-app-dev
```



## Додаткові команди

### Lint чарту

```bash
helm lint .
```

### Dry-run (без встановлення)

```bash
helm install course-app . -n course-app-dev --dry-run --debug
```

### Template rendering

```bash
helm template course-app . -n course-app-dev
```

### Пакування чарту

```bash
helm package .
```
