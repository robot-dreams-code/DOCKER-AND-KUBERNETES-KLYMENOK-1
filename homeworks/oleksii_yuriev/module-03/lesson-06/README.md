# Simple App 🐳


## Build image
```bash
docker build --no-cache -t lesson-05:1.0.0  -f homeworks/oleksii_yuriev/module-2/lesson-05/Dockerfile apps/course-app
[+] Building 10.6s (11/11) FINISHED                                                                                                                                                          docker:rancher-desktop
 => [internal] load build definition from Dockerfile                                                                                                                                                           0.0s
 => => transferring dockerfile: 362B                                                                                                                                                                           0.0s
 => [internal] load metadata for docker.io/library/python:3.14-alpine3.22                                                                                                                                      1.1s
 => [internal] load .dockerignore                                                                                                                                                                              0.0s
 => => transferring context: 2B                                                                                                                                                                                0.0s
 => [1/6] FROM docker.io/library/python:3.14-alpine3.22@sha256:8373231e1e906ddfb457748bfc032c4c06ada8c759b7b62d9c73ec2a3c56e710                                                                                0.0s
 => [internal] load build context                                                                                                                                                                              0.0s
 => => transferring context: 121B                                                                                                                                                                              0.0s
 => CACHED [2/6] WORKDIR /app                                                                                                                                                                                  0.0s
 => [3/6] COPY requirements.txt .                                                                                                                                                                              0.0s
 => [4/6] RUN pip install -r requirements.txt                                                                                                                                                                  7.5s
 => [5/6] COPY . .                                                                                                                                                                                             0.0s
 => [6/6] RUN adduser -D -u 1000 appuser      && chown -R appuser:appuser /app      &&  apk update && apk add curl                                                                                             1.7s
 => exporting to image                                                                                                                                                                                         0.2s
 => => exporting layers                                                                                                                                                                                        0.2s
 => => writing image sha256:16aa052fa132e335e8576527c219372239e7e1cf97ef82a086399014df475bca                                                                                                                   0.0s
 => => naming to docker.io/library/lesson-05:1.0.0
```

## Deploy Deployments & Services
```bash
kubectl apply -f deployment_app.yml
kubectl apply -f deployment_redis.yml
kubectl apply -f svc_app.yml
kubectl apply -f svc_redis.yml
```

## Check All in default namespace
```bash
kubectl get all                                                                                        󱃾 rancher-desktop
NAME                         READY   STATUS    RESTARTS   AGE
pod/app-7b554785d4-62bb7     1/1     Running   0          23m
pod/app-7b554785d4-g9v6g     1/1     Running   0          23m
pod/redis-86b8bf8458-ghv9k   1/1     Running   0          29m

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)          AGE
service/app          NodePort    10.43.172.175   <none>        8080:30080/TCP   21m
service/kubernetes   ClusterIP   10.43.0.1       <none>        443/TCP          17d
service/redis        ClusterIP   10.43.227.106   <none>        6379/TCP         23m

NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/app     2/2     2            2           23m
deployment.apps/redis   1/1     1            1           29m

NAME                               DESIRED   CURRENT   READY   AGE
replicaset.apps/app-7b554785d4     2         2         2       23m
replicaset.apps/redis-86b8bf8458   1         1         1       29m
```

## Check App
```bash
curl localhost:30080/healthz
{"status":"ok"}%

```
