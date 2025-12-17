# module-03/lesson-07 — Viktor Petrushenko

- 10 реплік
- ConfigMap → оновлення НЕ перезапускає поди автоматично
- Примусовий restart через `kubectl rollout restart`
- Оновлення імеджа → RollingUpdate
- Досліджено maxUnavailable/maxSurge + Recreate
- Доступ: http://$(minikube ip):30080
