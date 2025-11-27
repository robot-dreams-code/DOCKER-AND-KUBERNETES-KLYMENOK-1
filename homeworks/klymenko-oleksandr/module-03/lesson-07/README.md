# Homework: Module 03 / Lesson 07

### Збірка Dockerfile

```bash
docker build \
  -t course-app:1.0.1 \
  -f homeworks/klymenko-oleksandr/module-03/lesson-07/Dockerfile \
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
kubectl apply -n dev -f homeworks/klymenko-oleksandr/module-03/lesson-07/k8s/
```

### Перевірка

```bash
kubectl rollout status deployment/course-app -n dev

kubectl get pods -n dev -l app=course-app

kubectl get svc -n dev course-app
```

### Видалення

```bash
kubectl delete namespace dev
```

