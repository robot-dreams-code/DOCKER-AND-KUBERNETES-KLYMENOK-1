```
kubens dragonfly-operator-system
```

```
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
```

```
kyrylich@Kyrylos-Laptop lesson-12 % k api-resources | grep dragonfly
dragonflies  dragonflydb.io/v1alpha1  true Dragonfly
```

```
k apply -f dragonfly.yaml
```

Інстал чарту з оновленним  APP_REDIS_URL: redis://dragonfly.dragonfly-operator-system.svc.cluster.local:6379

```
helm upgrade --install course-app ./../lesson-11/course-app -n course-app-dev -f ./values.yaml
```

Перевірка запису в Dragonfly
```
k exec --tty -i dragonfly-0 -- bash
```

apply rbac
```
k apply -f rbac.yaml
```

```
kubectl auth can-i list dragonflies --as=system:serviceaccount:dragonfly-operator-system:db-viewer
kubectl auth can-i delete dragonflies --as=system:serviceaccount:dragonfly-operator-system:db-viewer
```