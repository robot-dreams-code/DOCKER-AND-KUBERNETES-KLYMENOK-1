# Lesson 12 CRD and RBAC

1. Install dragonfly operator:
```bash

kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
```
Check api-resources:
```bash
❯ kubectl api-resources | grep dragonfly
dragonflies          dragonflydb.io/v1alpha1           true         Dragonfly
```

2. Deploy dragonfly CRD:
```bash
kubectl create namespace dragonfly-system
kubectl apply -f ./homeworks/yarovskyi/module-4/lesson-12/dragonfly/dragonfly.yaml
```
Check dragonfly CRD and service:
```bash
❯ kubectl get crd | grep dragonfly
dragonflies.dragonflydb.io                  2025-12-08T20:25:42Z

❯ k get dragonfly
NAME        PHASE   ROLLING UPDATE   REPLICAS
dragonfly   Ready                    2

❯ kubectl get svc -n dragonfly-system
NAME        TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
dragonfly   ClusterIP   10.43.36.153   <none>        6379/TCP   25s
```

3. Run helm chart course-app:
```bash
helm install --create-namespace --namespace robotdreams course-app ./homeworks/yarovskyi/module-4/lesson-12/course-app
```

Check https://course-app.local

4. Deploy Role, ServiceAccount and RoleBinding for Dragonfly:
```bash
 kubectl apply -f ./homeworks/yarovskyi/module-4/lesson-12/dragonfly/role.yaml
 kubectl apply -f ./homeworks/yarovskyi/module-4/lesson-12/dragonfly/service-account.yaml
 kubectl apply -f ./homeworks/yarovskyi/module-4/lesson-12/dragonfly/role-binding.yaml
```

Check RBAC in namespace "dragonfly-system":
```bash
kubens dragonfly-system
```
```bash
❯ kubectl auth can-i list dragonflies --as=system:serviceaccount:dragonfly-system:db-viewer
yes
```
```bash
❯ kubectl auth can-i delete dragonflies --as=system:serviceaccount:dragonfly-system:db-viewer
no
```

5. Delete all resources:
```bash
helm uninstall course-app -n robotdreams
kubectl delete ns robotdreams
kubectl delete ns dragonfly-system
kubectl delete -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
```
