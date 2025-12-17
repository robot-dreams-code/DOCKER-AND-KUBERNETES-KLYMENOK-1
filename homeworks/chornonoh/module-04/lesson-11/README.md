# homework(module-04/lesson-11): Volodymyr Chornonoh

## Create the namespace

```bash
kubectl create namespace lesson-11
```

## Generate certificate

```bash
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout ./homeworks/chornonoh/module-04/lesson-11/course-app-local.key \
  -out ./homeworks/chornonoh/module-04/lesson-11/course-app-local.crt \
  -subj "/CN=course-app.local/O=course-app"
```

## Create a tls secret in kubernetes

```bash
kubectl create secret tls course-app-tls \
  --key ./homeworks/chornonoh/module-04/lesson-11/course-app-local.key \
  --cert ./homeworks/chornonoh/module-04/lesson-11/course-app-local.crt \
  -n lesson-11
```

## With internal database

```bash
helm install myapp ./homeworks/chornonoh/module-04/lesson-11/course-app \
  --namespace lesson-11 \
  --set redis.internal.enabled=true
```

```bash
kubectl get pods -n lesson-11
```

```txt
NAME                                READY   STATUS    RESTARTS   AGE
course-app-myapp-66c5ffbdfb-75pxs   1/1     Running   0          18s
course-app-myapp-66c5ffbdfb-8pfkf   1/1     Running   0          18s
course-app-myapp-66c5ffbdfb-d4pr6   1/1     Running   0          18s
course-app-myapp-66c5ffbdfb-jshgs   1/1     Running   0          18s
course-app-myapp-66c5ffbdfb-mprd4   1/1     Running   0          18s
course-app-myapp-66c5ffbdfb-n5kqh   1/1     Running   0          18s
course-app-myapp-66c5ffbdfb-rgp7f   1/1     Running   0          18s
course-app-myapp-66c5ffbdfb-wbnvh   1/1     Running   0          18s
course-app-myapp-66c5ffbdfb-x5kvs   1/1     Running   0          18s
course-app-myapp-66c5ffbdfb-xqkxr   1/1     Running   0          18s
course-app-myapp-redis-0            1/1     Running   0          18s
```

## With bitnami

```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

```bash
helm install redis bitnami/redis \
  --namespace lesson-11 \
  --create-namespace \
  --set architecture=standalone \
  --set auth.enabled=false
```

```bash
helm install with-bitnami ./homeworks/chornonoh/module-04/lesson-11/course-app \
  --namespace lesson-11 \
  --set redis.internal.enabled=false \
  --set redis.external.host=redis-master \
  --set redis.external.port=6379
```

```bash
kubectl get pods -n lesson-11
```

```txt
NAME                                      READY   STATUS    RESTARTS   AGE
course-app-with-bitnami-bfb696686-5cd9n   1/1     Running   0          31s
course-app-with-bitnami-bfb696686-5mtd6   1/1     Running   0          31s
course-app-with-bitnami-bfb696686-5sd2n   1/1     Running   0          31s
course-app-with-bitnami-bfb696686-5xcfr   1/1     Running   0          31s
course-app-with-bitnami-bfb696686-9kgrw   1/1     Running   0          31s
course-app-with-bitnami-bfb696686-b4ccv   1/1     Running   0          31s
course-app-with-bitnami-bfb696686-b7xfl   1/1     Running   0          31s
course-app-with-bitnami-bfb696686-v2tnt   1/1     Running   0          31s
course-app-with-bitnami-bfb696686-vxxgj   1/1     Running   0          31s
course-app-with-bitnami-bfb696686-zhbcz   1/1     Running   0          31s
redis-master-0                            1/1     Running   0          2m8s
```
