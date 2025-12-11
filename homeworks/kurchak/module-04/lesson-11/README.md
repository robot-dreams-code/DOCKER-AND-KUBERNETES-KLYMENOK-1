### Install Redis via Bitnami
```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
```

### Install Redis (single node, no password for simplicity):
```
helm install redis bitnami/redis --set architecture=standalone --set auth.enabled=false
```

#### Check:
```
kubectl get pods -l app.kubernetes.io/instance=redis
kubectl get svc redis-master
```

### Deploy the course-app chart
#### First, ensure the TLS secret exists (same hostname as in values):
```
$HOST="course-app.127.0.0.1.sslip.io"
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
-keyout tls.key -out tls.crt \
-subj "/CN=$HOST/O=CourseApp"
kubectl create secret tls course-app-tls \
--cert=tls.crt --key=tls.key
```

#### Shave values.yaml to match your needs (update image tag, replica count, ingress host, etc.). Then install:
```
helm install course-app ./course-app
```

#### Verify:
```
helm ls
kubectl get pods
kubectl get svc
kubectl get ingress course-app
```

#### Test access (if using sslip.io):
```
curl --resolve course-app.127.0.0.1.sslip.io:443:127.0.0.1 \
-k https://course-app.127.0.0.1.sslip.io
```

### Updating or uninstalling
#### Change values and upgrade:
```
helm upgrade course-app ./course-app
```

#### Rollback:
```
helm rollback course-app 1
```

#### Uninstall:
```
helm uninstall course-app
helm uninstall redis
```
