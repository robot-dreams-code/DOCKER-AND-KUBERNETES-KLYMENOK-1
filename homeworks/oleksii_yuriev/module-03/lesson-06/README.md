# Simple App 🐳


## Push image to docker hub
```bash
docker push yurievac/lesson-06:latest                                                                                                                                                                  28s
The push refers to repository [docker.io/yurievac/lesson-06]
1629e2a0b9ea: Pushed
8332f7a7e79b: Pushed
29fb752b176c: Pushed
640d3b83e65d: Pushed
2012aa1be4bf: Pushed
4a6d96fd2053: Mounted from library/python
2e2676b7c8f7: Mounted from library/python
ff2fefea59ce: Mounted from library/python
0e64f2360a44: Mounted from library/redis
latest: digest: sha256:eed120ff15a04115ce6d5aa25c1e24e83972839925a3bf3a89a147d8699eb453 size: 2201
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
