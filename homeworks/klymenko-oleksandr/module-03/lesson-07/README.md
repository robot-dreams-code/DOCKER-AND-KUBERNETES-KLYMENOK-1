# Homework: Module 03 / Lesson 07

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

