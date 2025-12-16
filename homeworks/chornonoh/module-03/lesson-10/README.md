# homework(module-03/lesson-10): Volodymyr Chornonoh

## Building and pushing the image

```bash
docker build \
    -f homeworks/chornonoh/module-03/lesson-10/Dockerfile \
    -t course-app \
    apps/course-app

docker tag course-app hbvhuwe/course-app:latest

docker push hbvhuwe/course-app:latest
```

## Checking the storage class

```bash
kubectl get sc
```

Output:

```txt
NAME                   PROVISIONER             RECLAIMPOLICY   VOLUMEBINDINGMODE      ALLOWVOLUMEEXPANSION   AGE
local-path (default)   rancher.io/local-path   Delete          WaitForFirstConsumer   false                  33d
```

## Create the namespace

```bash
kubectl create namespace lesson-10
```

## Creating database deployment & service

```bash
kubectl apply -f ./homeworks/chornonoh/module-03/lesson-10/database-statefulset.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-10/database-service.yaml
```

## Database status

```bash
kubectl get pods -n lesson-10
```

Output:

```txt
NAME         READY   STATUS    RESTARTS   AGE
database-0   1/1     Running   0          12s
```

```bash
kubectl get statefulset -n lesson-10
```

Output:

```txt
NAME       READY   AGE
database   1/1     34s
```

```bash
kubectl get service -n lesson-10
```

Output:

```txt
NAME       TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
database   ClusterIP   None         <none>        6379/TCP   67s
```

## Generate certificate

```bash
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout ./homeworks/chornonoh/module-03/lesson-10/course-app-local.key \
  -out ./homeworks/chornonoh/module-03/lesson-10/course-app-local.crt \
  -subj "/CN=course-app.local/O=course-app"
```

## Create a tls secret in kubernetes

```bash
kubectl create secret tls course-app-tls \
  --key ./homeworks/chornonoh/module-03/lesson-10/course-app-local.key \
  --cert ./homeworks/chornonoh/module-03/lesson-10/course-app-local.crt \
  -n lesson-10
```

To open the `course-app.local` in the browser I've added an entry in `/etc/hosts`:

```txt
127.0.0.1  course-app.local
```

## Creating course-app config map, deployment, service and ingress

```bash
kubectl apply -f ./homeworks/chornonoh/module-03/lesson-10/course-app-config-map.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-10/course-app-deployment.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-10/course-app-service.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-10/course-app-ingress.yaml
```

## Application status

```bash
kubectl get pods -n lesson-10
```

Output:

```txt
NAME                        READY   STATUS    RESTARTS   AGE
course-app-fdbfc8b7-2lz8l   0/1     Running   0          6s
course-app-fdbfc8b7-55d7n   0/1     Running   0          6s
course-app-fdbfc8b7-8d56l   0/1     Running   0          6s
course-app-fdbfc8b7-9dtn8   0/1     Running   0          6s
course-app-fdbfc8b7-jvt5n   0/1     Running   0          6s
course-app-fdbfc8b7-nhb2v   0/1     Running   0          6s
course-app-fdbfc8b7-q4n2k   0/1     Running   0          6s
course-app-fdbfc8b7-s2tdp   0/1     Running   0          6s
course-app-fdbfc8b7-v2bzc   0/1     Running   0          6s
course-app-fdbfc8b7-zj4z6   0/1     Running   0          6s
database-0                  1/1     Running   0          5m9s
```

```bash
kubectl get service -n lesson-10
```

Output:

```txt
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
course-app   ClusterIP   10.43.51.104   <none>        8080/TCP   27s
database     ClusterIP   None           <none>        6379/TCP   5m31s
```

```bash
kubectl get ingress -n lesson-10
```

Output:

```txt
NAME         CLASS     HOSTS              ADDRESS        PORTS     AGE
course-app   traefik   course-app.local   192.168.64.2   80, 443   40s
```
