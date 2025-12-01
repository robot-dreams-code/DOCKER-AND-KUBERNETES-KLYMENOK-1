# Lesson 06 Kubernetes Deployment and Service

1. Create a config-map:
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-07/config-map.yaml
```

2. Deploy Redis Deployment and Service:
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-07/deployment-redis.yaml
kubectl apply -f homeworks/yarovskyi/module-2/lesson-07/service-redis.yaml
```

3. Deploy Course-App Deployment and Service:
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-07/deployment-course-app.yaml
kubectl apply -f homeworks/yarovskyi/module-2/lesson-07/service-course-app.yaml
```
Check app by going to http://localhost:30080. Check if the message the same as in config-map.

4. Update the APP_MESSAGE value in config-map.yaml and deploy it.
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-07/config-map.yaml
```
Check http://localhost:30080. The message should be the same as previous.

5. Restart deployment:
```bash
kubectl rollout status deployment course-app
```
Check http://localhost:30080. The message should be as updated in config-map.yaml.

6. Pull the new image tag into docker hub. There are two image tags:
```bash
yarovskiy/course-app:1.0.0
yarovskiy/course-app (latest)
```

7. Check rollout status during deploying the new image tag
```bash
$ kubectl rollout status deployment course-app
Waiting for deployment "course-app" rollout to finish: 2 out of 10 new replicas have been updated...
Waiting for deployment "course-app" rollout to finish: 3 out of 10 new replicas have been updated...
Waiting for deployment "course-app" rollout to finish: 4 out of 10 new replicas have been updated...
Waiting for deployment "course-app" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "course-app" rollout to finish: 6 out of 10 new replicas have been updated...
Waiting for deployment "course-app" rollout to finish: 7 out of 10 new replicas have been updated...
Waiting for deployment "course-app" rollout to finish: 8 out of 10 new replicas have been updated...
Waiting for deployment "course-app" rollout to finish: 9 out of 10 new replicas have been updated...
Waiting for deployment "course-app" rollout to finish: 2 old replicas are pending termination...
Waiting for deployment "course-app" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "course-app" rollout to finish: 9 of 10 updated replicas are available...
deployment "course-app" successfully rolled out
```

8. Check Recreate strategy:
```bash
  strategy:
    type: Recreate
```
All pods will be deleted and new pods will be created. During ~10-15 seconds, the app will be unavailable.

9. Check RollingUpdate strategy:
```bash
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 1
      maxUnavailable: 1
```
During the update, the pods will be updated one by one.
```bash
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 25%
```
During the update, every 2 pods will terminate and 2-3 pods will be created. 
