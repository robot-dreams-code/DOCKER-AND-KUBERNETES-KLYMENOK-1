# homework(module-03/lesson-08): Volodymyr Chornonoh

## Building and pushing the image

```bash
docker build \
    -f homeworks/chornonoh/module-03/lesson-08/Dockerfile \
    -t course-app \
    apps/course-app

docker tag course-app hbvhuwe/course-app:latest

docker push hbvhuwe/course-app:latest
```

## Create the namespace

```bash
kubectl create namespace lesson-08
```

## Creating database deployment & service

```bash
kubectl apply -f ./homeworks/chornonoh/module-03/lesson-08/database-deployment.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-08/database-service.yaml
```

## Database status

```bash
kubectl get pods -n lesson-08
```

Output:

```txt
NAME                        READY   STATUS    RESTARTS   AGE
database-86c8bd5bc6-q9s7d   1/1     Running   0          6s
```

```bash
kubectl get service -n lesson-08
```

Output:
```txt
NAME       TYPE        CLUSTER-IP   EXTERNAL-IP   PORT(S)    AGE
database   ClusterIP   None         <none>        6379/TCP   24s
```

## Generate certificate

```bash
openssl req -x509 -nodes -days 365 \
  -newkey rsa:2048 \
  -keyout ./homeworks/chornonoh/module-03/lesson-08/course-app-local.key \
  -out ./homeworks/chornonoh/module-03/lesson-08/course-app-local.crt \
  -subj "/CN=course-app.local/O=course-app"
```

## Create a tls secret in kubernetes

```bash
kubectl create secret tls course-app-tls \
  --key ./homeworks/chornonoh/module-03/lesson-08/course-app-local.key \
  --cert ./homeworks/chornonoh/module-03/lesson-08/course-app-local.crt \
  -n lesson-08
```

To open the `course-app.local` in the browser I've added an entry in `/etc/hosts`:

```txt
127.0.0.1  course-app.local
```

## Creating course-app config map, deployment, service and ingress

```bash
kubectl apply -f ./homeworks/chornonoh/module-03/lesson-08/course-app-config-map.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-08/course-app-deployment.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-08/course-app-service.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-08/course-app-ingress.yaml
```

## Application status

```bash
kubectl get pods -n lesson-08
```

Output:

```txt
NAME                        READY   STATUS    RESTARTS   AGE
course-app-fdbfc8b7-8sjlq   1/1     Running   0          17s
course-app-fdbfc8b7-9k7h5   1/1     Running   0          17s
course-app-fdbfc8b7-cvmkw   1/1     Running   0          17s
course-app-fdbfc8b7-hbssm   1/1     Running   0          17s
course-app-fdbfc8b7-j84x4   1/1     Running   0          17s
course-app-fdbfc8b7-l8ggd   1/1     Running   0          17s
course-app-fdbfc8b7-m77k5   1/1     Running   0          17s
course-app-fdbfc8b7-nk979   1/1     Running   0          17s
course-app-fdbfc8b7-qjr5d   1/1     Running   0          17s
course-app-fdbfc8b7-vn6t6   1/1     Running   0          17s
database-86c8bd5bc6-q9s7d   1/1     Running   0          105s
```

```bash
kubectl get service -n lesson-08
```

Output:
```txt
NAME         TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
course-app   ClusterIP   10.43.199.34   <none>        8080/TCP   35s
database     ClusterIP   None           <none>        6379/TCP   2m3s
```

```bash
kubectl get ingress -n lesson-08
```

Output:
```txt
NAME         CLASS     HOSTS              ADDRESS        PORTS     AGE
course-app   traefik   course-app.local   192.168.64.2   80, 443   93s
```
