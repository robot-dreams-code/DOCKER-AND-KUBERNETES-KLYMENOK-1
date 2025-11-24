# Lesson 08 Kubernetes Deployment and Service

1. Deploy a config-map:
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-08/config-map.yaml
```

2. Deploy Redis Deployment and Service:
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-08/deployment-redis.yaml
kubectl apply -f homeworks/yarovskyi/module-2/lesson-08/service-redis.yaml
```

3. Deploy Course-App Deployment and Service:
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-08/deployment-course-app.yaml
kubectl apply -f homeworks/yarovskyi/module-2/lesson-08/service-course-app.yaml
```

4. Create secret with tls:
```bash
kubectl create secret tls course-app-tls --cert=homeworks/yarovskyi/module-2/lesson-08/cert/course-app.local.crt --key=homeworks/yarovskyi/module-2/lesson-08/cert/course-app.local.key
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
kubectl apply -f homeworks/yarovskyi/module-2/lesson-08/ingress.yaml
```
Check https://course-app.local

7. Check readinessProbe:
```bash
kubectl get endpoints course-app-sv
```
Run pod's container bash and kill process:
```bash
kubectl exec -it {pod} -- bash
> kill 1
```
Check endpoints again. The pod's ip will be removed from the list.
