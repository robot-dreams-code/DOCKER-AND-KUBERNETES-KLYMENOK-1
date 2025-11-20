# homework(module-03/lesson-06): Volodymyr Chornonoh

## Building and pushing the image

```bash
docker build \
    -f homeworks/chornonoh/module-03/lesson-06/Dockerfile \
    -t lesson-06-course-app \
    apps/course-app

docker tag lesson-06-course-app hbvhuwe/lesson-06-course-app:latest

docker push hbvhuwe/lesson-06-course-app:latest
```

## Starting a deployment

```bash
kubectl create namespace lesson-06

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-06/deployment.yaml

kubectl apply -f ./homeworks/chornonoh/module-03/lesson-06/service.yaml
```

## Getting pods status

```bash
kubectl get pods -n lesson-06
```

Example output:

```txt
NAME                          READY   STATUS    RESTARTS   AGE
course-app-7697d5bdb7-54lp6   1/1     Running   0          4m3s
course-app-7697d5bdb7-xwth4   1/1     Running   0          3m59s
```

```bash
kubectl get services -n lesson-06
```

```txt
NAME         TYPE       CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
course-app   NodePort   10.43.52.246   <none>        8080:30080/TCP   2m2s
```

## Changing replicas count

```bash
kubectl apply -f ./homeworks/chornonoh/module-03/lesson-06/deployment.yaml

kubectl rollout status deployment/course-app -n lesson-06

kubectl get pods -n lesson-06
```

Example output:

```text
deployment "course-app" successfully rolled out
```

```text
NAME                          READY   STATUS    RESTARTS   AGE
course-app-54584bd99c-4kqm4   1/1     Running   0          7s
course-app-54584bd99c-8lhsj   1/1     Running   0          38s
course-app-54584bd99c-mgxrq   1/1     Running   0          100s
course-app-54584bd99c-rg4rj   1/1     Running   0          102s
course-app-54584bd99c-z5486   1/1     Running   0          7s
```

## Cleanup

```bash
kubectl delete deployment course-app -n lesson-06
```

```txt
deployment.apps "course-app" deleted from lesson-06 namespace
```

```bash
kubectl delete service course-app -n lesson-06
```

```txt
service "course-app" deleted from lesson-06 namespace
```

```bash
kubectl delete namespace lesson-06
```

```txt
namespace "lesson-06" deleted
```
