## 1. Використаємо спрощену версію деплою з попередніх уроків.
```bash
kubectl get storageclass
kubectl get pods -n local-path-storage
```
```
NAME                                      READY   STATUS    RESTARTS   AGE
local-path-provisioner-7d6dddf9dd-ptpkh   1/1     Running   0          95s
```

## 2. Створимо і опишемо readis ресурси.


## 3. Задеплоємо додаток.
```bash
kubectl apply -f ./
kubectl get pods 
```
```
NAME                                     READY   STATUS    RESTARTS   AGE
course-app-deployment-85977596f7-44dnl   1/1     Running   0          10s
course-app-deployment-85977596f7-cnl28   1/1     Running   0          10s
course-app-deployment-85977596f7-nzdcf   1/1     Running   0          10s
redis-0                                  1/1     Running   0          9s
```

## 4. Перевіримо застосунок в вебі. Впевнемося що він працює коректно
