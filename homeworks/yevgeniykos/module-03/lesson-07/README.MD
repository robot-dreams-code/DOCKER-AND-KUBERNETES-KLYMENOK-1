# KUBERNETES

Додаємо ConfgiMap у наш yaml для нашої аппки

Додаємо Strategy

strategy:
    type: RollingUpdate
    rollingUpdate:
      maxUnavailable: 20%
      maxSurge: 30%  

PS: в якості експеримента використовув і відсоткові значення і числові

Для того щоб почати Rollout

`kubectl set image deployment/course-app-deployment\ course-app=rdlsolutions/course-app:1.0.1 -n mod03-less06`

Слідкуваати за процесом оновлення

`kubectl rollout status deployment/my-app`

Щоб провернути оновлення на попередню версію імеджу

`kubectl rollout undo deployment/my-app`
