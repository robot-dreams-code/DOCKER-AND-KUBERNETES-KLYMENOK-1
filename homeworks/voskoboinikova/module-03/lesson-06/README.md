#Запушити зібраний імедж для apps/course-app у Docker Hub або GitHub Registry
Використала demo.goharbor.io через обмежння корпоративного середовища
##using demo.goharbor.io because of corporate restrictions
docker login demo.goharbor.io
docker tag course-app:v1.0 demo.goharbor.io/lesson06/course-app:v1.0
docker push demo.goharbor.io/lesson06/course-app:v1.0

#Задеплоїти ресурси в Rancher Desktop кластер
##Перевірка 
###kubectl get nodes
NAME         STATUS   ROLES                  AGE   VERSION
ho-pc02352   Ready    control-plane,master   17d   v1.33.5+k3s1

##Задеплоїти ресурси
###kubectl apply -f deployment.yaml
deployment.apps/course-app created

###kubectl apply -f service.yaml
service/course-app-nodeport created

##Перевірка 
###kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
course-app-7fb49bc4df-rvjqt   1/1     Running   0          2m21s
course-app-7fb49bc4df-xgv9m   1/1     Running   0          2m21s

###kubectl get svc
NAME                  TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE
NAME                  TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)          AGE
course-app-nodeport   NodePort    10.43.154.82   <none>        8080:30080/TCP   69s
kubernetes            ClusterIP   10.43.0.1      <none>        443/TCP          17d

###kubectl get deployments
NAME         READY   UP-TO-DATE   AVAILABLE   AGE
course-app   2/2     2            2           5m9s


#Змінити кількість реплік у deployment.yaml, передеплоїти та подивитися на процес оновлення (kubectl rollout status deployment/<NAME>)
###kubectl apply -f deployment.yaml
deployment.apps/course-app configured


###kubectl rollout status deployment/course-app
Waiting for deployment "course-app" rollout to finish: 4 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 5 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 6 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 7 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 8 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 9 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 10 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 11 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 12 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 13 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 14 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 15 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 16 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 17 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 18 of 20 updated replicas are available...
Waiting for deployment "course-app" rollout to finish: 19 of 20 updated replicas are available...
deployment "course-app" successfully rolled out
