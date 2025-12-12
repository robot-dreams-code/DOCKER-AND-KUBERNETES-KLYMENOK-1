# Simple App 🐳

## Check StorageClasses
```bash
kubectl get sc
NAME                   PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  32d
```

## Check PVC (Before Deployment)
```bash
kubectl get pvc
No resources found in default namespace.
```

## Deploy Redis StatefulSet and Verify Resources
```bash
kubectl apply -f redis-statefulset.yml
statefulset.apps/redis created

kubectl get all
NAME                      READY   STATUS    RESTARTS      AGE
pod/app-d6f58dcc5-45m4j   1/1     Running   3 (12m ago)   3d13h
pod/app-d6f58dcc5-6t5lh   1/1     Running   3 (12m ago)   3d13h
pod/app-d6f58dcc5-9pw8h   1/1     Running   3 (12m ago)   3d13h
pod/app-d6f58dcc5-bd5kh   1/1     Running   3 (12m ago)   3d13h
pod/app-d6f58dcc5-j6x8p   1/1     Running   3 (12m ago)   3d13h
pod/app-d6f58dcc5-k5n58   1/1     Running   3 (12m ago)   3d13h
pod/app-d6f58dcc5-spmzg   1/1     Running   3 (12m ago)   3d13h
pod/app-d6f58dcc5-stwb2   1/1     Running   3 (12m ago)   3d13h
pod/app-d6f58dcc5-v2fxv   1/1     Running   3 (12m ago)   3d13h
pod/app-d6f58dcc5-zgfqt   1/1     Running   3 (12m ago)   3d13h
pod/redis-0               1/1     Running   0             7m47s
pod/redis-1               1/1     Running   0             7m42s
pod/redis-2               1/1     Running   0             7m37s

NAME                 TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/app          ClusterIP   10.43.160.127   <none>        8080/TCP   6d
service/kubernetes   ClusterIP   10.43.0.1       <none>        443/TCP    32d
service/redis        ClusterIP   10.43.247.9     <none>        6379/TCP   6d

NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/app   10/10   10           10          6d

NAME                             DESIRED   CURRENT   READY   AGE
replicaset.apps/app-6b9799f974   0         0         0       6d
replicaset.apps/app-8bd669d69    0         0         0       4d22h
replicaset.apps/app-d6f58dcc5    10        10        10      3d13h

NAME                     READY   AGE
statefulset.apps/redis   3/3     7m47s
```

## Check PVC and PV
```bash
kubectl get pvc
NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data-redis-0   Bound    pvc-3835cd46-9343-4497-8860-832c62f83e6a   1Gi        RWO            local-path     <unset>                 3m25s
redis-data-redis-1   Bound    pvc-427bbbbd-13bf-4d66-9847-da1baeb1ae6e   1Gi        RWO            local-path     <unset>                 3m20s
redis-data-redis-2   Bound    pvc-13a3c64a-5488-46ab-abb4-090c472f9445   1Gi        RWO            local-path     <unset>                 3m15s


kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                        STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-13a3c64a-5488-46ab-abb4-090c472f9445   1Gi        RWO            Delete           Bound    default/redis-data-redis-2   local-path     <unset>                          3m14s
pvc-3835cd46-9343-4497-8860-832c62f83e6a   1Gi        RWO            Delete           Bound    default/redis-data-redis-0   local-path     <unset>                          3m24s
pvc-427bbbbd-13bf-4d66-9847-da1baeb1ae6e   1Gi        RWO            Delete           Bound    default/redis-data-redis-1   local-path     <unset>                          3m19s
```
