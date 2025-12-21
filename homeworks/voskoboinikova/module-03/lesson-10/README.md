#make sure that StorageClass is accessible in our cluster in Rancher Desktop
kubectl get sc

NAME                   PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  24d


#apply changes
kubectl apply -f namespace.yaml
kubectl apply -f k8s/redis-statefulset.yaml
kubectl apply -f . 
kubectl get pods -n lesson10

NAME                          READY   STATUS    RESTARTS   AGE
course-app-696584cd7d-27htd   1/1     Running   0          31s
course-app-696584cd7d-2jrxm   1/1     Running   0          31s
course-app-696584cd7d-4cgtw   1/1     Running   0          31s
course-app-696584cd7d-65tth   1/1     Running   0          31s
course-app-696584cd7d-7qlk7   1/1     Running   0          31s
course-app-696584cd7d-c2kvz   1/1     Running   0          31s
course-app-696584cd7d-hmtk7   1/1     Running   0          31s
course-app-696584cd7d-pqqlg   1/1     Running   0          31s
course-app-696584cd7d-sllkw   1/1     Running   0          31s
course-app-696584cd7d-tlng7   1/1     Running   0          31s
redis-0                       1/1     Running   0          77s

kubectl get pvc
NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data-redis-0   Bound    pvc-e036d52f-7741-4631-897e-a7757b20148d   1Gi        RWO            local-path     <unset>                 106m

kubectl get pv 
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS        CLAIM                                   STORAGECLASS   VOLUMEATTRIBUTESCLASS   REASON   AGE
pvc-c9330f7c-ac1a-414d-8dcb-7659f5693b9c   1Gi        RWO            Delete           Bound         lesson10/redis-data-redis-0             local-path     <unset>                          42m
