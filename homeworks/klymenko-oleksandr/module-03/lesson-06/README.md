# Homework: Module 02 / Lesson 06

### Збірка Dockerfile

```bash
docker build \
  -t course-app:1.0.0 \
  -f homeworks/klymenko-oleksandr/module-3/lesson-06/Dockerfile \
  apps/course-app
```

# Тег Docker Hub

```bash
export DOCKER_USER=ЛОГИН_DOCKER_HUB
docker tag course-app:1.0.0 $DOCKER_USER/course-app:1.0.0
```

### Логін та push

```bash
docker login
docker push $DOCKER_USER/course-app:1.0.0
```



### Запуск kubernets

```bash
kubectl create namespace dev
kubectl apply -n dev -f homeworks/klymenko-oleksandr/module-3/lesson-06/k8s/
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

