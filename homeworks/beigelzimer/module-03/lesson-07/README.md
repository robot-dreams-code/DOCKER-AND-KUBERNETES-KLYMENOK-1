#Описати Deployment з мінімум 10 репліками.
#kubectl apply -f .
deployment.apps/course-app created
service/course-app-nodeport created
configmap/web-config created

#Змінити значення у ConfigMap і перевірити, як оновлюються Pods.
#kubectl rollout restart deployment/course-app
kubectl get pods --watch
NAME                          READY   STATUS              RESTARTS   AGE
course-app-5d9fb8465-8vhvc    1/1     Running             0          5s
course-app-5d9fb8465-b9q8k    1/1     Running             0          4s
course-app-5d9fb8465-cwx7t    0/1     ContainerCreating   0          1s
course-app-5d9fb8465-l79t5    1/1     Running             0          2s
course-app-5d9fb8465-rt2mj    1/1     Running             0          4s
course-app-5d9fb8465-w694p    1/1     Running             0          5s
course-app-5d9fb8465-xw2jd    0/1     ContainerCreating   0          1s
course-app-5d9fb8465-xx6vw    1/1     Running             0          3s
course-app-5d9fb8465-zdr59    1/1     Running             0          2s
course-app-6d76b99684-fh79x   1/1     Running             0          119s
course-app-6d76b99684-p4xvl   1/1     Terminating         0          116s
course-app-6d76b99684-p4xvl   0/1     Completed           0          116s
course-app-5d9fb8465-xw2jd    1/1     Running             0          1s
course-app-5d9fb8465-cwx7t    1/1     Running             0          1s
course-app-6d76b99684-fh79x   1/1     Terminating         0          119s
course-app-6d76b99684-p4xvl   0/1     Completed           0          116s
course-app-6d76b99684-p4xvl   0/1     Completed           0          116s
course-app-5d9fb8465-97794    0/1     Pending             0          0s
course-app-5d9fb8465-97794    0/1     Pending             0          0s
course-app-5d9fb8465-97794    0/1     ContainerCreating   0          0s
course-app-6d76b99684-fh79x   0/1     Completed           0          2m
course-app-6d76b99684-fh79x   0/1     Completed           0          2m
course-app-6d76b99684-fh79x   0/1     Completed           0          2m
course-app-5d9fb8465-97794    1/1     Running             0          1s

#Оновити образ контейнера та простежити rollout
#kubectl rollout status deployment/course-app
Waiting for deployment "course-app" rollout to finish: 9 out of 10 new replicas have been updated...
Waiting for deployment "course-app" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "course-app" rollout to finish: 9 of 10 updated replicas are available...
deployment "course-app" successfully rolled out

#Дослідити поведінку RollingUpdate з різними значеннями maxUnavailable, maxSurge. Спробувати Replace стратегію. Пояснити їх переваги та недоліки та відмінність між ними
RollingUpdate 
Переваги: можливість завершення поточних сессій, мінімальний downtime, поступова заміна
Недоліки: висока складність ПЗ, низка швидкість заміни (залежить від maxUnavailable, maxSurge)

Recreate
Переваги: менша складність ПЗ, висока швидкість заміни
Недоліки: необхідність зупинки обробки
