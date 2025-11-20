# homework-07

За основу цієї домашки взяв файли с meretskyi/module-03/lesson-06/

1. Оновив Deployment для створення 10 реплік
```
kyrylich@Kyrylos-Laptop lesson-07 % k get pods -n course-app-dev
NAME                                     READY   STATUS    RESTARTS   AGE
course-app-deployment-64985466d9-2x8lp   1/1     Running   0          2m36s
course-app-deployment-64985466d9-6gwfp   1/1     Running   0          2m36s
course-app-deployment-64985466d9-92fz6   1/1     Running   0          2m39s
course-app-deployment-64985466d9-94wzq   1/1     Running   0          2m39s
course-app-deployment-64985466d9-jr5tt   1/1     Running   0          2m39s
course-app-deployment-64985466d9-k7q65   1/1     Running   0          2m39s
course-app-deployment-64985466d9-nfpxc   1/1     Running   0          2m36s
course-app-deployment-64985466d9-qpfb8   1/1     Running   0          2m36s
course-app-deployment-64985466d9-r2xpb   1/1     Running   0          2m36s
course-app-deployment-64985466d9-r5b9f   1/1     Running   0          2m39s
```

2. Створив ConfigMap
При зміні значення в `data.HELLO_MESSAGE` і після запуску `k apply` поди не оновлються.  
Для застосування значення з ConfigMap запустив `k rollout restart deployment/course-app-deployment -n course-app-dev`
3. Очевидно, але чекнув додатково
```yaml
          env:
            - name: APP_MESSAGE
              valueFrom:
                configMapKeyRef:
                  name: course-app-config-map 
                  key: REVERSED_HELLO_MESSAGE # Якщо змінювати ключ з ConfigMap, то при k apply, значення застосовується.
```
Перевірка результату зміни APP_MESSAGE - $.message 
`curl http://localhost:30080/api/info | jq`
```
{
  "app": "course-app",
  "hostname": "course-app-deployment-64985466d9-92fz6",
  "store": "sqlite",
  "db_path": "data/data.sql",
  "redis_url": "",
  "messages_api": "",
  "counter_api": "",
  "message": "!iykstereM olyryK morf krowemoh s'ti ,olleH",
  "secret_token_present": false,
  "env": {
    "APP_MESSAGE": "!iykstereM olyryK morf krowemoh s'ti ,olleH"
  }
}
```

4. Додав Rolling Update
   kyrylich@Kyrylos-Laptop lesson-07 % k apply -f dev -n course-app-dev                         
   configmap/course-app-config-map unchanged
   deployment.apps/course-app-deployment configured
   namespace/course-app-dev unchanged
   service/course-app-svc unchanged

   kyrylich@Kyrylos-Laptop lesson-07 % k get pods -n course-app-dev    
   NAME                                     READY   STATUS              RESTARTS   AGE
   course-app-deployment-6597d99597-6nhcl   0/1     Completed           0          3m38s
   course-app-deployment-6597d99597-72mz6   1/1     Running             0          3m38s
   course-app-deployment-6597d99597-drd2l   1/1     Running             0          3m35s
   course-app-deployment-6597d99597-fk9j7   1/1     Running             0          3m35s
   course-app-deployment-6597d99597-jrzgb   1/1     Running             0          3m38s
   course-app-deployment-6597d99597-m4bhv   1/1     Running             0          3m35s
   course-app-deployment-6597d99597-m7fms   1/1     Running             0          3m38s
   course-app-deployment-6597d99597-mkkx7   1/1     Running             0          3m38s
   course-app-deployment-6597d99597-rptkq   0/1     Completed           0          48s
   course-app-deployment-7c856c77b8-7m6fh   0/1     ContainerCreating   0          1s
   course-app-deployment-7c856c77b8-djdvx   0/1     ContainerCreating   0          1s
   course-app-deployment-7c856c77b8-dsvxs   0/1     ContainerCreating   0          1s
   course-app-deployment-7c856c77b8-pqv6x   0/1     ContainerCreating   0          1s
   course-app-deployment-7c856c77b8-x8rks   0/1     ContainerCreating   0          1s
   kyrylich@Kyrylos-Laptop lesson-07 % k get pods -n course-app-dev
   NAME                                     READY   STATUS              RESTARTS   AGE
   course-app-deployment-6597d99597-72mz6   1/1     Running             0          3m40s
   course-app-deployment-6597d99597-drd2l   1/1     Running             0          3m37s
   course-app-deployment-6597d99597-fk9j7   1/1     Terminating         0          3m37s
   course-app-deployment-6597d99597-jrzgb   1/1     Terminating         0          3m40s
   course-app-deployment-6597d99597-m4bhv   1/1     Terminating         0          3m37s
   course-app-deployment-6597d99597-m7fms   1/1     Running             0          3m40s
   course-app-deployment-6597d99597-mkkx7   1/1     Terminating         0          3m40s
   course-app-deployment-7c856c77b8-7m6fh   1/1     Running             0          3s
   course-app-deployment-7c856c77b8-cvwwr   0/1     ContainerCreating   0          0s
   course-app-deployment-7c856c77b8-djdvx   1/1     Running             0          3s
   course-app-deployment-7c856c77b8-dsvxs   1/1     Running             0          3s
   course-app-deployment-7c856c77b8-kbj4g   0/1     ContainerCreating   0          0s
   course-app-deployment-7c856c77b8-pqv6x   1/1     Running             0          3s
   course-app-deployment-7c856c77b8-q5l4r   0/1     ContainerCreating   0          0s
   course-app-deployment-7c856c77b8-x8rks   1/1     Running             0          3s
   kyrylich@Kyrylos-Laptop lesson-07 % k get pods -n course-app-dev
   NAME                                     READY   STATUS              RESTARTS   AGE
   course-app-deployment-6597d99597-72mz6   1/1     Running             0          3m42s
   course-app-deployment-6597d99597-drd2l   1/1     Running             0          3m39s
   course-app-deployment-7c856c77b8-7m6fh   1/1     Running             0          5s
   course-app-deployment-7c856c77b8-7mg7h   0/1     ContainerCreating   0          2s
   course-app-deployment-7c856c77b8-7rp9l   0/1     ContainerCreating   0          2s
   course-app-deployment-7c856c77b8-cvwwr   0/1     ContainerCreating   0          2s
   course-app-deployment-7c856c77b8-djdvx   1/1     Running             0          5s
   course-app-deployment-7c856c77b8-dsvxs   1/1     Running             0          5s
   course-app-deployment-7c856c77b8-kbj4g   0/1     ContainerCreating   0          2s
   course-app-deployment-7c856c77b8-pqv6x   1/1     Running             0          5s
   course-app-deployment-7c856c77b8-q5l4r   0/1     ContainerCreating   0          2s
   course-app-deployment-7c856c77b8-x8rks   1/1     Running             0          5s
   kyrylich@Kyrylos-Laptop lesson-07 % k get pods -n course-app-dev
   NAME                                     READY   STATUS              RESTARTS   AGE
   course-app-deployment-6597d99597-72mz6   1/1     Terminating         0          3m43s
   course-app-deployment-6597d99597-drd2l   1/1     Terminating         0          3m40s
   course-app-deployment-7c856c77b8-7m6fh   1/1     Running             0          6s
   course-app-deployment-7c856c77b8-7mg7h   1/1     Running             0          3s
   course-app-deployment-7c856c77b8-7rp9l   1/1     Running             0          3s
   course-app-deployment-7c856c77b8-cvwwr   0/1     ContainerCreating   0          3s
   course-app-deployment-7c856c77b8-djdvx   1/1     Running             0          6s
   course-app-deployment-7c856c77b8-dsvxs   1/1     Running             0          6s
   course-app-deployment-7c856c77b8-kbj4g   1/1     Running             0          3s
   course-app-deployment-7c856c77b8-pqv6x   1/1     Running             0          6s
   course-app-deployment-7c856c77b8-q5l4r   0/1     ContainerCreating   0          3s
   course-app-deployment-7c856c77b8-x8rks   1/1     Running             0          6s
   kyrylich@Kyrylos-Laptop lesson-07 % k get pods -n course-app-dev
   NAME                                     READY   STATUS    RESTARTS   AGE
   course-app-deployment-7c856c77b8-7m6fh   1/1     Running   0          7s
   course-app-deployment-7c856c77b8-7mg7h   1/1     Running   0          4s
   course-app-deployment-7c856c77b8-7rp9l   1/1     Running   0          4s
   course-app-deployment-7c856c77b8-cvwwr   1/1     Running   0          4s
   course-app-deployment-7c856c77b8-djdvx   1/1     Running   0          7s
   course-app-deployment-7c856c77b8-dsvxs   1/1     Running   0          7s
   course-app-deployment-7c856c77b8-kbj4g   1/1     Running   0          4s
   course-app-deployment-7c856c77b8-pqv6x   1/1     Running   0          7s
   course-app-deployment-7c856c77b8-q5l4r   1/1     Running   0          4s
   course-app-deployment-7c856c77b8-x8rks   1/1     Running   0          7s


5. Змінив на Recreate

kyrylich@Kyrylos-Laptop lesson-07 % k apply -f dev -n course-app-dev
configmap/course-app-config-map unchanged
deployment.apps/course-app-deployment configured
namespace/course-app-dev unchanged
service/course-app-svc unchanged
kyrylich@Kyrylos-Laptop lesson-07 % ls                              
kyrylich@Kyrylos-Laptop lesson-07 %  k get pods -n course-app-dev

NAME                                     READY   STATUS        RESTARTS   AGE
course-app-deployment-7c856c77b8-7mg7h   1/1     Terminating   0          10h
course-app-deployment-7c856c77b8-7rp9l   0/1     Completed     0          10h
course-app-deployment-7c856c77b8-cvwwr   0/1     Completed     0          10h
course-app-deployment-7c856c77b8-djdvx   0/1     Completed     0          10h
course-app-deployment-7c856c77b8-dsvxs   0/1     Completed     0          10h
course-app-deployment-7c856c77b8-q5l4r   0/1     Completed     0          10h
course-app-deployment-7c856c77b8-x8rks   0/1     Completed     0          10h

kyrylich@Kyrylos-Laptop lesson-07 %  k get pods -n course-app-dev
NAME                                     READY   STATUS              RESTARTS   AGE
course-app-deployment-6597d99597-2xkzj   0/1     ContainerCreating   0          2s
course-app-deployment-6597d99597-c9jnw   0/1     ContainerCreating   0          2s
course-app-deployment-6597d99597-dc57n   0/1     ContainerCreating   0          2s
course-app-deployment-6597d99597-nvrml   0/1     ContainerCreating   0          2s
course-app-deployment-6597d99597-pg69m   0/1     ContainerCreating   0          2s
course-app-deployment-6597d99597-s2h68   0/1     ContainerCreating   0          2s
course-app-deployment-6597d99597-vgdt2   0/1     ContainerCreating   0          2s
course-app-deployment-6597d99597-vl8jf   0/1     ContainerCreating   0          2s
course-app-deployment-6597d99597-x64q4   0/1     ContainerCreating   0          2s
course-app-deployment-6597d99597-xt5gw   0/1     ContainerCreating   0          2s

kyrylich@Kyrylos-Laptop lesson-07 %  k get pods -n course-app-dev
NAME                                     READY   STATUS    RESTARTS   AGE
course-app-deployment-6597d99597-2xkzj   1/1     Running   0          5s
course-app-deployment-6597d99597-c9jnw   1/1     Running   0          5s
course-app-deployment-6597d99597-dc57n   1/1     Running   0          5s
course-app-deployment-6597d99597-nvrml   1/1     Running   0          5s
course-app-deployment-6597d99597-pg69m   1/1     Running   0          5s
course-app-deployment-6597d99597-s2h68   1/1     Running   0          5s
course-app-deployment-6597d99597-vgdt2   1/1     Running   0          5s
course-app-deployment-6597d99597-vl8jf   1/1     Running   0          5s
course-app-deployment-6597d99597-x64q4   1/1     Running   0          5s
course-app-deployment-6597d99597-xt5gw   1/1     Running   0          5s



Rolling Update
Pros
- Немає full down time, частково заміняємо старі поди на нові
Cons
- Не підходить, коли нам треба мати тільки одну версію бекенду.
Наприклад, ми патчимо клієнти(девайси) на конкретну версію беку.
Якщо якісь контейнери будуть старої версії, то клієнти можуть крашитись.


Recreate
- Підходить, коли є час на down time, наприклад для сервісів, які мають визначені working / maintenance hours