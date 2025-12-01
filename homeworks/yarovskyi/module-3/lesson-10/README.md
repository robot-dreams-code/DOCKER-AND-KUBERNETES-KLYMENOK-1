# Lesson 10 Kubernetes Persistent Storage

1. Deploy a config-map:
```bash
kubectl apply -f homeworks/yarovskyi/module-3/lesson-10/config-map.yaml
```

2. Deploy Redis Statefulset and Service:
```bash
kubectl apply -f homeworks/yarovskyi/module-3/lesson-10/redis-statefulset.yaml
kubectl apply -f homeworks/yarovskyi/module-3/lesson-10/redis-service.yaml
```
Check existed storageClass and created pvc and pv:
```bash
kubectl get sc
kubectl get pvc
kubectl get pv
```

3. Deploy Course-App Deployment, HorizontalPodAutoscaler and Service:
```bash
kubectl apply -f homeworks/yarovskyi/module-3/lesson-10/course-app-deployment.yaml
kubectl apply -f homeworks/yarovskyi/module-3/lesson-10/course-app-hpa.yaml
kubectl apply -f homeworks/yarovskyi/module-3/lesson-10/course-app-service.yaml
```

4. Create secret with tls:
```bash
kubectl create secret tls course-app-tls --cert=homeworks/yarovskyi/module-3/lesson-10/cert/course-app.local.crt --key=homeworks/yarovskyi/module-3/lesson-10/cert/course-app.local.key
```

5. Add custom host into /etc/hosts:
```bash
 $ kubectl get ingress -A
NAMESPACE     NAME                 CLASS     HOSTS              ADDRESS        PORTS     AGE
robotdreams   course-app-ingress   traefik   course-app.local   192.168.64.2   80, 443   37m
```
Add into /etc/hosts:
```bash
192.168.64.2 course-app.local
```

6. Deploy Ingress:
```bash
kubectl apply -f homeworks/yarovskyi/module-3/lesson-10/ingress.yaml
```
Check https://course-app.local
