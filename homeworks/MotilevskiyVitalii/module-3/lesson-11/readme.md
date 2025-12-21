Launch
=====

1) ``cd homeworks/MotilevskiyVitalii/module-3/lesson-11``
2) ``helm repo add bitnami https://charts.bitnami.com/bitnami``
3) ``helm repo update``
4) ``kubectl create namespace course || true``
5) ```
   helm upgrade --install redis bitnami/redis \
   --namespace course \
   --set architecture=standalone \
   --set auth.enabled=false
6) ``cd course-app``
7) ```
   helm upgrade --install course-app . \
   --namespace course \
   --create-namespace
   ```
8) Check status
 ```
   kubectl -n course get pods
   kubectl -n course get svc
   kubectl -n course get ingress
```
9) Add hosts http://test.example.loc/