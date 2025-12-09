# 1. Перенесемо файли ingress.yaml, deployment.yaml, service.yaml з попередніх завдань.


# 2. Для початку знайдемо офіційний репозиторій - https://github.com/dragonflydb/dragonfly-operator, і ознайомимось з документацією.


# 3. Встановимо dragonfly-operator:
```bash
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
```
```
get pods -n dragonfly-operator-system
NAME                                                    READY   STATUS    RESTARTS   AGE
dragonfly-operator-controller-manager-97cdfcc85-dgl2n   2/2     Running   0          45s

kubectl get crd | grep dragonfly
dragonflies.dragonflydb.io                  2025-12-07T11:03:18Z

kubectl api-resources | grep dragonfly
dragonflies                                      dragonflydb.io/v1alpha1             true         Dragonfly
```


# 3. Створимо dragonfly.yaml, змінимо env деплойменту, проведемо деплой застосунку:
```bash
kubectl apply -f ./
```
```
kubectl get dragonfly
NAME        PHASE   ROLLING UPDATE   REPLICAS
dragonfly   Ready                    2

kubectl get pods
NAME                                    READY   STATUS    RESTARTS   AGE
course-app-deployment-cdb9fc5f8-4mdbl   1/1     Running   0          58s
course-app-deployment-cdb9fc5f8-prwmf   1/1     Running   0          58s
course-app-deployment-cdb9fc5f8-sjkqd   1/1     Running   0          58s
dragonfly-0                             1/1     Running   0          58s
dragonfly-1                             1/1     Running   0          43s

get svc
NAME             TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
course-app-svc   ClusterIP   10.43.75.228   <none>        80/TCP     67s
dragonfly        ClusterIP   10.43.94.40    <none>        6379/TCP   67s
kubernetes       ClusterIP   10.43.0.1      <none>        443/TCP    107s
```


# 4. Відкривши http://course-app.local/ вдостовіримось, що додаток дійсно працює.


# 5. Опишемо service-account, role, binding згідно з завданням, та застосуємо їх.
```bash
kubectl apply -f dragonfly-sa.yaml -f dragonfly-role.yaml -f dragonfly-binding.yaml
```


# 6. Перевіримо надані доступи.
```bash
kubectl auth can-i get dragonflies --as=system:serviceaccount:default:db-viewer
kubectl auth can-i delete dragonflies --as=system:serviceaccount:default:db-viewer
```
```
yes
no
```
