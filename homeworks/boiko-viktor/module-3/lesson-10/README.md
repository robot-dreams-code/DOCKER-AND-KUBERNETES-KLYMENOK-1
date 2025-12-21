## Створення Namespace

створюємо namespace:
```bash
k apply -f namespace.yml
```

## Деплой ресурсів

Застосуємо всі конфігураційні файли (ConfigMap, Deployment, Service, Ingress, Middleware, Secret, Redis-StatefulSet):
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
- **Redis-StatefulSet**: `redis-course-app` (1 реплік).
- **Service**: `redis-course-app-svc` (ClusterIP).

## встановлюємо нейм спейс по дефолту
```bash
k config set-context --current --namespace=course-app-dev
```

Перевіряємо статус подів та PVC (PersistentVolumeClaim):
```bash
k get pods
NAME                                     READY   STATUS    RESTARTS      AGE
course-app-deployment-8649596657-429xz   1/1     Running   1 (39m ago)   39m
course-app-deployment-8649596657-7tn65   1/1     Running   1 (39m ago)   39m
course-app-deployment-8649596657-9ljrp   1/1     Running   1 (39m ago)   39m
course-app-deployment-8649596657-db4fx   1/1     Running   1 (39m ago)   39m
course-app-deployment-8649596657-fs5qx   1/1     Running   1 (39m ago)   39m
course-app-deployment-8649596657-pdhvq   1/1     Running   1 (39m ago)   39m
course-app-deployment-8649596657-qkxl2   1/1     Running   1 (39m ago)   39m
course-app-deployment-8649596657-rl988   1/1     Running   1 (39m ago)   39m
course-app-deployment-8649596657-rmrjn   1/1     Running   1 (39m ago)   39m
course-app-deployment-8649596657-z4tlx   1/1     Running   1 (39m ago)   39m
redis-course-app-0                       1/1     Running   0             39m

k get pvc
NAME                            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data-redis-course-app-0   Bound    pvc-a34e1bfc-e81b-443a-a5d8-71333e25c0a7   1Gi        RWO            local-path     <unset>                 40m
```

Перевіряємо логи додатку, щоб переконатися у підключенні до Redis:
```bash
k logs -l app=course-app
INFO:     10.42.0.1:41756 - "GET /healthz HTTP/1.1" 200 OK
INFO:     10.42.0.1:53476 - "GET /readyz HTTP/1.1" 200 OK
```
перевіряємо записи в редіс бд
```bash
k exec -it redis-course-app-0 -- redis-cli
127.0.0.1:6379> keys *
1) "counters:visits"

127.0.0.1:6379> get counters:visits
"16"
```   
Видаляємо редіс:
```bash
k delete -f redis-statefulset.yaml
```
застосовуємо ресурси заново щоб перевірити данні на диску змонтвоаному в под редіс:

```bash
k apply -f redis-statefulset.yaml
k exec -it redis-course-app-0 -- redis-cli
127.0.0.1:6379> get counters:visits
"16"
```
все працює як і очікувались дані збереглись на диску, при видалені кластера видаляється і диск це також перевірено

### невеликий експеремент з репліками в редіс поставив 3 репліки, результат наступний(отримали тридиска, кожен на свій под, фле данні пишуться на один є підозра що при навантаженні можуть писатись на різні і це не ок) :

```bash
 k get pods | grep redis
redis-course-app-0                       1/1     Running   0               6m3s
redis-course-app-1                       1/1     Running   0               5m56s
redis-course-app-2                       1/1     Running   0               5m50s

 k get pvc
NAME                            STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data-redis-course-app-0   Bound    pvc-fd2ade29-1f9b-4c9e-80e6-04a2d91043a3   1Gi        RWO            local-path     <unset>                 114s
redis-data-redis-course-app-1   Bound    pvc-b1c01f79-3fe1-4c5a-a00d-1c16063b0f89   1Gi        RWO            local-path     <unset>                 107s
redis-data-redis-course-app-2   Bound    pvc-77f96292-d972-4a63-b120-8081cba4998b   1Gi        RWO            local-path     <unset>                 101s

k exec -it redis-course-app-1 -- redis-cli
127.0.0.1:6379> get counters:visits
(nil)
127.0.0.1:6379> exit

k exec -it redis-course-app-2 -- redis-cli
127.0.0.1:6379> get counters:visits
(nil)
127.0.0.1:6379> exit

k exec -it redis-course-app-0 -- redis-cli
127.0.0.1:6379> get counters:visits
"41"
127.0.0.1:6379> exit

```
Видаляємо ресурси:
```bash
k delete -f namespace.yml
```