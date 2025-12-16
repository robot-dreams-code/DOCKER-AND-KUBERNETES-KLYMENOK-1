### multi-arch

```bash
docker buildx build `
  --platform linux/amd64,linux/arm64 `
  -t kyle21/course-app:1.0.1 `
  -f homeworks/klymenko-oleksandr/module-03/lesson-10/Dockerfile `
  apps/course-app `
  --push
```


# Homework: Module 04 / Lesson 11


## 1. Швидкий запуск (всі команди разом)

```bash
# 1) Namespace + репозиторій чартів
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update

# 2) Redis від Bitnami
helm upgrade --install redis bitnami/redis `
  -n dev `
  -f homeworks/klymenko-oleksandr/module-04/lesson-11/helm/redis-values.yaml

# 3) Власний чарт застосунку
$env:DOCKER_USER='kyle21'

helm upgrade --install course-app `
  homeworks/klymenko-oleksandr/module-04/lesson-11/helm/course-app `
  -n dev `
  --set image.repository="$env:DOCKER_USER/course-app" `
  --set image.tag=1.0.1 `
  --set image.pullPolicy=Always

# 4) Перевірка доступності сервісів/ingress
kubectl logs deploy/course-app-course-app -n dev
kubectl get pods,svc,ingress -n dev

# 5) Опційно: перевірити застосунок через порт
kubectl port-forward svc/course-app-course-app -n dev 8080:8080
curl http://localhost:8080
```

### Видалення

```bash
kubectl delete namespace dev
```