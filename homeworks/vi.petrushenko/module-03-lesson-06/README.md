# module-03/lesson-06 – Viktor Petrushenko

- Імедж: `vtsvetnoy/course-app:latest` (запушено в Docker Hub)
- Deployment з 3 репліками + livenessProbe
- Service типу NodePort → доступний на http://localhost:30080
- Перевірено масштабування та rollout

Запуск:
```bash
kubectl apply -f deployment.yaml -f service.yaml
kubectl rollout status deployment/course-app
