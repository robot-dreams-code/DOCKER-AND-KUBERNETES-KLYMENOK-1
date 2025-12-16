# Homework: Module 03 / Lesson 08

### Збірка Dockerfile

```bash
docker build \
  -t course-app:1.0.1 \
  -f homeworks/klymenko-oleksandr/module-03/lesson-08/Dockerfile \
  apps/course-app
```

# Тег Docker Hub

```bash
export DOCKER_USER=kyle21
docker tag course-app:1.0.1 $DOCKER_USER/course-app:1.0.1
```

### Логін та push

```bash
docker login
docker push $DOCKER_USER/course-app:1.0.1
```


### Запуск kubernets

```bash
kubectl create namespace dev
kubectl apply -n dev -f homeworks/klymenko-oleksandr/module-03/lesson-08/k8s/
```

### Видалення

```bash
kubectl delete namespace dev
```

### Перевірка

```bash
kubectl rollout status deployment/course-app -n dev

kubectl get pods -n dev -l app=course-app

kubectl get svc -n dev course-app

kubectl get ingress -n dev

kubectl get endpoints -n dev

kubectl get secrets -n dev

kubectl describe ingress course-app-ingress -n dev
```



### Zero Downtime Test:

  ### отказ readiness 
  # readinessProbe:
  #   httpGet:
  #     path: /broken

  # Після цього Pod переходив у стан NotReady, але продовжував працювати.
  # У результаті IP цього Pod-а зникав зі списку endpoint-ів:

### Переірка IP + Ready
```bash
kubectl get endpointslice course-app-vpbgj -n dev -o jsonpath='{range .endpoints[*]}{.addresses}{" READY="}{.conditions.ready}{"\n"}{end}'
```






### Згенерувати TLS Secret

```bash
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout tls.key \
  -out tls.crt \
  -subj "/CN=course-app.local/O=course-app"
```

### Створив TLS Secret у namespace dev

```bash
kubectl create secret tls course-app-tls \
  --key tls.key \
  --cert tls.crt \
  -n dev
```

