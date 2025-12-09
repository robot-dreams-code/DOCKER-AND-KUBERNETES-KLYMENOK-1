Основні команди
===============

`kubectl apply -f deployment.yaml` - запустити деплой і підняття подів  
`kubectl get pods` - переглянути статус pods  
`kubectl get rs` - інформація про replicaSet  
`kubectl scale deployment course-app-motilevskiy --replicas=0` - зупинити всі pods  
` kubectl port-forward svc/course-app-motilevskiy 30080:8080` - Пробросити порт назовні щоб був доступ до кластера по http

Урок 8

Додати сертифікати
1) Згенерувати tls key вказати Common name "test.example.loc" `openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt`
2) Додати сертифікати в kuber `kubectl create secret tls course-app-motilevskiy-tls --key=tls.key --cert=tls.crt`
3) Додати на хост машині хост `test.example.loc`
4) Перейти по https://test.example.loc

Щоб зімітувати помилку в 1 поді можна зсилатися на зчитування файлу (тільки для демонстрації)
1) Змінюємо конфіг для deployment
    ```
    readinessProbe:
        exec:
          command: ['sh', '-c', 'test -f /tmp/ready']
   ```
2) `kubectl apply -f deployment.yaml`
3) `kubectl rollout restart deployment course-config-motilevskiy`
4) Бачимо що жодна пода не в статусі ready `kubectl get pods`
5) Додаємо файл на поду `kubectl exec -it <podName> -- sh -c 'touch /tmp/ready'`
6) Через 5 секунд бачимо що пода в статусі ready `kubectl get pods`
7) Бачимо що ip поди з'явився в endpoints `kubectl get endpoints course-app-motilevskiy`
8) Видаляємо файл `kubectl exec -it <podName> -- sh -c 'rm /tmp/ready'`
9) Через 5 секунд бачимо що пода в статусі not ready `kubectl get pods`
10) Бачимо що ip поди зник з endpoints `kubectl get endpoints course-app-motilevskiy`