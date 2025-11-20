# robot_dreams :: Lessons-06

## Overview

Створюємо наш окремий Namespace і змінюємо поточний контекст для зручності:
```bash
kubectl apply -f namespace.yml
kubectl config set-context --current --namespace=robot-dreams
```

Ініціюємо створенна ресурсів типу Deployment

```bash
kubectl apply -f redis.deployment.yml
kubectl apply -f redis.svc.yml

kubectl apply -f app.deployment.yml
kubectl apply -f app.svc.yml
```

Тепер можна переглянути наявність і деталі

```bash
kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
app-deployment     1/1     1            1           8m47s
redis-deployment   1/1     1            1           8m57s

kubectl get services
NAME        TYPE        CLUSTER-IP        EXTERNAL-IP   PORT(S)          AGE
app-svc     NodePort    192.168.194.157   <none>        8080:30080/TCP   8m56s
redis-svc   ClusterIP   192.168.194.239   <none>        6379/TCP         9m6s

kubectl get pods
NAME                                READY   STATUS    RESTARTS   AGE
app-deployment-77dd6f69c6-5vc9k     1/1     Running   0          42s
redis-deployment-86cdd4b6cd-mvhpn   1/1     Running   0          8m26s
```

Тепер спробуємо зробити скейл

```bash
kubectl apply -f app.deployment.yml
kubectl rollout status deployment/app-deployment
```

І побачимо що все спрацювало:
```bash
kubectl get pods -l app=app
NAME                              READY   STATUS    RESTARTS   AGE
app-deployment-77dd6f69c6-5vc9k   1/1     Running   0          10m
app-deployment-77dd6f69c6-nsh4z   1/1     Running   0          2m33s
app-deployment-77dd6f69c6-wqjm7   1/1     Running   0          2m33s
```