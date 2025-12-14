# homework(module-03/lesson-07): Volodymyr Chornonoh

## Building and pushing the image

```bash
docker build \
    -f homeworks/chornonoh/module-03/lesson-07/Dockerfile \
    -t course-app \
    apps/course-app

docker tag course-app hbvhuwe/course-app:latest

docker push hbvhuwe/course-app:latest
```

## Create the namespace

```bash
kubectl create namespace lesson-07
```

## Creating database volume claim, deployment & service

```bash
kubectl apply -f ./homeworks/chornonoh/module-03/lesson-07/database-pv-claim.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-07/database-deployment.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-07/database-service.yaml
```

## Database status

```bash
kubectl get pods -n lesson-07
```

Output:

```txt
NAME                        READY   STATUS    RESTARTS   AGE
database-86c8bd5bc6-cj96v   1/1     Running   0          6m11s
```

```bash
kubectl get service -n lesson-07
```

Output:
```txt
NAME       TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
database   ClusterIP   None         <none>        6379/TCP   8m12s
```

## Creating course-app config map, deployment & service

```bash
kubectl apply -f ./homeworks/chornonoh/module-03/lesson-07/course-app-config-map.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-07/course-app-deployment.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-07/course-app-service.yaml
```

## Application status

```bash
kubectl get pods -n lesson-07
```

Output:

```txt
NAME                          READY   STATUS    RESTARTS   AGE
course-app-5b6d975ffb-2lmjl   1/1     Running   0          63s
course-app-5b6d975ffb-4f78t   1/1     Running   0          63s
course-app-5b6d975ffb-7f26z   1/1     Running   0          63s
course-app-5b6d975ffb-87ngz   1/1     Running   0          63s
course-app-5b6d975ffb-948mm   1/1     Running   0          63s
course-app-5b6d975ffb-nmfzn   1/1     Running   0          63s
course-app-5b6d975ffb-q2j5k   1/1     Running   0          63s
course-app-5b6d975ffb-rkz2f   1/1     Running   0          63s
course-app-5b6d975ffb-vxvrr   1/1     Running   0          63s
course-app-5b6d975ffb-wm9v9   1/1     Running   0          63s
database-86c8bd5bc6-cj96v     1/1     Running   0          9m20s
```

```bash
kubectl get service -n lesson-07
```

Output:
```txt
NAME         TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
course-app   NodePort    10.43.144.143   <none>        8080:30080/TCP   2m2s
database     ClusterIP   None            <none>        6379/TCP         10m
```
