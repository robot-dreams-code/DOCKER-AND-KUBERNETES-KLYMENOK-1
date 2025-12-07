# robot_dreams :: Lessons-10

## Аналіз StorageClass

Перевіряємо наявність і склад StorageClass в нашому кластері:

```bash
kubectl get sc
NAME                   PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  12d
```

То ж не потрібно робити якихось додаткових операцій по зміні налаштувань кластеру.

## Redis як StatefulSet

Підготувавши відповідні файли (redis.pvc.yml, redis.statefulset.yml) - опрацьовуємо розгортання сервісу Redis з зберіганням поточного стану через PVC

```bash
❯ kubectl get pvc
No resources found in lesson-10 namespace.

# Створюємо наш PVC
❯ kubectl apply -f redis.pvc.yml
persistentvolumeclaim/redis-data created

# Перевіряємо стан
❯ kubectl get pvc
NAME         STATUS    VOLUME   CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data   Pending                                      local-path     <unset>                 2s

❯ kubectl describe pvc redis-data
Name:          redis-data
Namespace:     lesson-10
StorageClass:  local-path
Status:        Pending
Volume:
Labels:        <none>
Annotations:   <none>
Finalizers:    [kubernetes.io/pvc-protection]
Capacity:
Access Modes:
VolumeMode:    Filesystem
Used By:       <none>
Events:
  Type    Reason                Age                  From                         Message
  ----    ------                ----                 ----                         -------
  Normal  WaitForFirstConsumer  6s (x15 over 3m26s)  persistentvolume-controller  waiting for first consumer to be created before binding

# Застосовуємо наш новий StatefulSet
❯ kubectl apply -f redis.statefulset.yml
statefulset.apps/redis-statefulset created

# Перевіряємо наявність змін
❯ kubectl get pvc
NAME                             STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data                       Pending                                                                        local-path     <unset>                 87s
redis-data-redis-statefulset-0   Bound     pvc-0f98e347-d93a-4e9a-82f3-e046a9bb9d54   1Gi        RWO            local-path     <unset>                 49s
redis-data-redis-statefulset-1   Bound     pvc-4c7db948-4ef0-4a6f-9754-e6d3c31f2265   1Gi        RWO            local-path     <unset>                 19s
redis-data-redis-statefulset-2   Bound     pvc-1cdbc4d7-ffe7-417b-9664-4c65b428c2ee   1Gi        RWO            local-path     <unset>                 14s
```

##

Застосовуємо всі наші компоненти і перевіряємо наявність відповідних записів в нашому кластері всередині поточного неймспейсу (lesson-10):

```bash
❯ kubectl get all
NAME                                  READY   STATUS    RESTARTS   AGE
pod/app-deployment-6658d898b9-bvfsv   1/1     Running   0          17s
pod/app-deployment-6658d898b9-wddwh   1/1     Running   0          17s
pod/app-deployment-6658d898b9-xrn4w   1/1     Running   0          17s
pod/redis-statefulset-0               1/1     Running   0          9m50s
pod/redis-statefulset-1               1/1     Running   0          5m20s
pod/redis-statefulset-2               1/1     Running   0          5m15s

NAME                TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
service/app-svc     ClusterIP   10.43.225.247   <none>        8080/TCP   30s
service/redis-svc   ClusterIP   10.43.64.90     <none>        6379/TCP   116s

NAME                             READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/app-deployment   3/3     3            3           17s

NAME                                        DESIRED   CURRENT   READY   AGE
replicaset.apps/app-deployment-6658d898b9   3         3         3       17s

NAME                                 READY   AGE
statefulset.apps/redis-statefulset   3/3     9m50s

❯ kubectl get pvc
NAME                             STATUS    VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data                       Pending                                                                        local-path     <unset>                 13m
redis-data-redis-statefulset-0   Bound     pvc-0f98e347-d93a-4e9a-82f3-e046a9bb9d54   1Gi        RWO            local-path     <unset>                 12m
redis-data-redis-statefulset-1   Bound     pvc-4c7db948-4ef0-4a6f-9754-e6d3c31f2265   1Gi        RWO            local-path     <unset>                 7m57s
redis-data-redis-statefulset-2   Bound     pvc-1cdbc4d7-ffe7-417b-9664-4c65b428c2ee   1Gi        RWO            local-path     <unset>                 7m52s

❯ kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                      STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-0f98e347-d93a-4e9a-82f3-e046a9bb9d54   1Gi        RWO            Delete           Bound    lesson-10/redis-data-redis-statefulset-0   local-path     <unset>                          12m
pvc-1cdbc4d7-ffe7-417b-9664-4c65b428c2ee   1Gi        RWO            Delete           Bound    lesson-10/redis-data-redis-statefulset-2   local-path     <unset>                          7m51s
pvc-4c7db948-4ef0-4a6f-9754-e6d3c31f2265   1Gi        RWO            Delete           Bound    lesson-10/redis-data-redis-statefulset-1   local-path     <unset>                          7m56s
```