## 1. Запушимо образ в DockerHub з nickdikiy/module-02/lesson-04:
```bash
docker login -u nickdikiynd
docker build -f ../../module-02/lesson-04/Dockerfile -t course-app ../../../../apps/course-app 
docker tag course-app nickdikiynd/course-app:1.0
docker push nickdikiynd/course-app:1.0  
```

## 2. Запустимо k8s кластер і перевіримо контекст:
```bash
orb start k8s
kubectl config get-contexts
```
```
CURRENT   NAME       CLUSTER    AUTHINFO   NAMESPACE
*         orbstack   orbstack   orbstack
```

## 3. Перевіримо існуючі namespaces:
```bash
kubectl get namespaces
```
```
NAME              STATUS   AGE
default           Active   9m10s
kube-node-lease   Active   9m10s
kube-public       Active   9m10s
kube-system       Active   9m10s
```

## 4. Так, як я хочу використовувати кастомний namespace, його необхідно створити:
```bash
kubectl create namespace homework
```
```
namespace/homework created
```
#### Namespace можна створити описавши yaml файл і виконавши команду kubectl apply. Гадаю цей підхід є більш практичним, тому:
```bash
kubectl delete ns homework
kubectl apply -f namespace.yaml
```
```
namespace "homework" deleted
namespace/homework created
```

## 5. Запустимо деплоймент:
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```
#### Запускати кожен файл окремо не зручно, тому вказуватимемо директорію:
```bash
kubectl apply -f ./
```
#### Зіштовхуємось із проблемою що namespace не існує, скоріше всього через рандомний порядок. Можна виправити використовуючи kustomization.yaml
```bash
kubectl apply -k .
```
```
namespace/homework created
service/course-app-nodeport created
deployment.apps/course-app-deployment created
```


## 6. Перевіримо дейлой:
```bash
kubectl get deployments -n homework
kubectl get service -n homework 
kubectl get pods -n homework

```
```
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
course-app-deployment   1/1     1            1           7m24s

NAME                  TYPE       CLUSTER-IP        EXTERNAL-IP   PORT(S)        AGE
course-app-nodeport   NodePort   192.168.194.169   <none>        80:30080/TCP   7m59s

NAME                                    READY   STATUS    RESTARTS   AGE
course-app-deployment-f6f8b9b7f-qq5xn   1/1     Running   0          8m52s
```
#### Важливо, ми вказуємо targetPort: 8080 в service.yaml, тому що додаток слухає саме цей порт.


## 7. Перевіримо що додаток працює. Також можна просто відкрити в браузері.
```bash
curl -o /dev/null -s -w "%{http_code}\n" http://localhost:30080
```


## 8. Змінимо replicaset і передеплоємо додаток:
```bash
kubectl apply -f deployment.yaml
kubectl get deployments -n homework
kubectl get pods -n homework

```
```
NAME                    READY   UP-TO-DATE   AVAILABLE   AGE
course-app-deployment   3/3     3            3           5m55s

NAME                                     READY   STATUS    RESTARTS   AGE
course-app-deployment-76d7779784-kp686   1/1     Running   0          2m5s
course-app-deployment-76d7779784-tx2j9   1/1     Running   0          7m42s
course-app-deployment-76d7779784-w6mzr   1/1     Running   0          2m5s
```

#### Для візуалізації роботи команди rollout збільшимо кількість реплік до 11:
```bash
kubectl rollout status deployment/course-app-deployment -n homework
kubectl describe deployment/course-app-deployment -n homework
```
```
Waiting for deployment "course-app-deployment" rollout to finish: 6 of 11 updated replicas are available...
Waiting for deployment "course-app-deployment" rollout to finish: 7 of 11 updated replicas are available...
Waiting for deployment "course-app-deployment" rollout to finish: 8 of 11 updated replicas are available...
Waiting for deployment "course-app-deployment" rollout to finish: 9 of 11 updated replicas are available...
Waiting for deployment "course-app-deployment" rollout to finish: 10 of 11 updated replicas are available...
deployment "course-app-deployment" successfully rolled out
```
```
Name:                   course-app-deployment
Namespace:              homework
CreationTimestamp:      Mon, 17 Nov 2025 20:30:37 +0200
Labels:                 <none>
Annotations:            deployment.kubernetes.io/revision: 1
Selector:               app=course-app
Replicas:               11 desired | 11 updated | 11 total | 11 available | 0 unavailable
StrategyType:           RollingUpdate
MinReadySeconds:        0
RollingUpdateStrategy:  25% max unavailable, 25% max surge
Pod Template:
  Labels:  app=course-app
  Containers:
   course-app:
    Image:         nickdikiynd/course-app:1.0
    Port:          80/TCP
    Host Port:     0/TCP
    Environment:   <none>
    Mounts:        <none>
  Volumes:         <none>
  Node-Selectors:  <none>
  Tolerations:     <none>
Conditions:
  Type           Status  Reason
  ----           ------  ------
  Progressing    True    NewReplicaSetAvailable
  Available      True    MinimumReplicasAvailable
OldReplicaSets:  <none>
NewReplicaSet:   course-app-deployment-76d7779784 (11/11 replicas created)
Events:
  Type    Reason             Age    From                   Message
  ----    ------             ----   ----                   -------
  Normal  ScalingReplicaSet  15m    deployment-controller  Scaled up replica set course-app-deployment-76d7779784 from 0 to 1
  Normal  ScalingReplicaSet  9m26s  deployment-controller  Scaled up replica set course-app-deployment-76d7779784 from 1 to 3
  Normal  ScalingReplicaSet  3m21s  deployment-controller  Scaled up replica set course-app-deployment-76d7779784 from 3 to 5
  Normal  ScalingReplicaSet  2m26s  deployment-controller  Scaled up replica set course-app-deployment-76d7779784 from 5 to 11
```
