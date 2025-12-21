# homework-10

Налаштував app-redis.yaml з Service і StatefulSet
На автоматі оновив ConfigMap з адресом контейнеру Redis (redis://redis:6379), не завелось. 
Згадав, що вхідною точкою є сервіс, оновив до redis://app-redis-svc:6379, запрацювало.

Перевірив чи оновлює додаток Redis
```
kyrylich@Kyrylos-Laptop dev % kubectl exec -it app-redis-0 -- redis-cli

127.0.0.1:6379> SCAN 0
1) "0"
2) 1) "counters:visits"
127.0.0.1:6379> get counters:visits
"1"
127.0.0.1:6379> get counters:visits
"2"
127.0.0.1:6379> get counters:visits
"3"
```

Чекнув Persistence Volume

```
kyrylich@Kyrylos-Laptop dev % k get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM                                   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-14051dd1-477f-4ee6-9f67-53bdd0d4cb06   1Gi        RWO            Delete           Bound    n8n-workshop/postgres-data-postgres-0   local-path     <unset>                          9d
pvc-d4f59f84-7232-4d6e-991f-7276188b6a5e   1Gi        RWO            Delete           Bound    course-app-dev/redis-data-app-redis-0   local-path     <unset>                          10m
```

```
kyrylich@Kyrylos-Laptop dev % k describe pv pvc-d4f59f84-7232-4d6e-991f-7276188b6a5e
Name:              pvc-d4f59f84-7232-4d6e-991f-7276188b6a5e
Labels:            <none>
Annotations:       local.path.provisioner/selected-node: lima-rancher-desktop
pv.kubernetes.io/provisioned-by: rancher.io/local-path
Finalizers:        [kubernetes.io/pv-protection]
StorageClass:      local-path
Status:            Bound
Claim:             course-app-dev/redis-data-app-redis-0
Reclaim Policy:    Delete
Access Modes:      RWO
VolumeMode:        Filesystem
Capacity:          1Gi
Node Affinity:     
Required Terms:  
Term 0:        kubernetes.io/hostname in [lima-rancher-desktop]
Message:           
Source:
Type:  LocalVolume (a persistent volume backed by local storage on a node)
Path:  /var/lib/rancher/k3s/storage/pvc-d4f59f84-7232-4d6e-991f-7276188b6a5e_course-app-dev_redis-data-app-redis-0
Events:    <none>
```