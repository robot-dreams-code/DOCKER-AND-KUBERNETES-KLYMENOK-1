# homework(module-04/lesson-12): Volodymyr Chornonoh

## Create the namespace

```bash
kubectl create namespace lesson-12
```

## Installing the dragonfly operator

```bash
git clone https://github.com/dragonflydb/dragonfly-operator.git
cd dragonfly-operator

helm install dragonfly-operator charts/dragonfly-operator \
    --namespace dragonfly-operator-system \
    --create-namespace
```

```bash
kubectl api-resources | grep dragonfly
```

Sample output:

```txt
dragonflies                                      dragonflydb.io/v1alpha1             true         Dragonfly
```

## Installing dragonfly

```bash
kubectl apply -f ./homeworks/chornonoh/module-04/lesson-12/dragonfly.yaml -n lesson-12
```

```bash
kubectl get pods -n lesson-12
```

Sample output:

```txt
NAME                 READY   STATUS    RESTARTS   AGE
dragonfly-sample-0   1/1     Running   0          49s
```

## Creating course-app config map, deployment and service

```bash
kubectl apply -f ./homeworks/chornonoh/module-04/lesson-12/course-app-config-map.yaml

kubectl apply -f ./homeworks/chornonoh/module-04/lesson-12/course-app-deployment.yaml

kubectl apply -f ./homeworks/chornonoh/module-04/lesson-12/course-app-service.yaml
```

```bash
kubectl get pods -n lesson-12
```

Sample output:

```txt
NAME                          READY   STATUS    RESTARTS   AGE
course-app-764f8ffbbf-fs4bd   1/1     Running   0          105s
dragonfly-sample-0            1/1     Running   0          9m4s
```

## RBAC

```bash
kubectl apply -f ./homeworks/chornonoh/module-04/lesson-12/rbac.yaml
```

Created resources:

```bash
kubectl get sa -n lesson-12
```

```txt
NAME        SECRETS   AGE
db-viewer   0         21s
default     0         11m
```

```bash
kubectl get role -n lesson-12
```

```txt
NAME          CREATED AT
db-readonly   2025-12-11T15:28:26Z
```

```bash
kubectl get rolebinding -n lesson-12
```

```txt
NAME                  ROLE               AGE
db-readonly-binding   Role/db-readonly   42s
```

## Checking permissions

```bash
kubectl auth can-i list dragonflies --as=system:serviceaccount:lesson-12:db-viewer -n lesson-12
```

Output: -> `yes`

```bash
kubectl auth can-i delete dragonflies --as=system:serviceaccount:lesson-12:db-viewer -n lesson-12
```

Output: -> `no`
