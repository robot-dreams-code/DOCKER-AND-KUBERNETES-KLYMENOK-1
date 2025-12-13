Розбирався з хельмом разом з АІшкою. Суть уловив. (скріншот працюючої апки прикріпив)
```
k get pods
```
```
NAME                                  READY   STATUS    RESTARTS        AGE
my-snak-app-redis-master-0            1/1     Running   0               7m6s
snak-app-deployment-bc5b49548-4qzcz   1/1     Running   5 (5m26s ago)   7m6s
snak-app-deployment-bc5b49548-6vgkz   1/1     Running   5 (5m29s ago)   7m6s
snak-app-deployment-bc5b49548-8qbxt   1/1     Running   5 (5m37s ago)   7m6s
snak-app-deployment-bc5b49548-9hcfv   1/1     Running   5 (5m26s ago)   7m6s
snak-app-deployment-bc5b49548-cmtpf   1/1     Running   5 (5m36s ago)   7m6s
snak-app-deployment-bc5b49548-ds4pm   1/1     Running   5 (5m33s ago)   7m6s
snak-app-deployment-bc5b49548-g5fjj   1/1     Running   5 (5m17s ago)   7m6s
snak-app-deployment-bc5b49548-g977t   1/1     Running   5 (5m39s ago)   7m6s
snak-app-deployment-bc5b49548-kh4bd   1/1     Running   5 (5m27s ago)   7m6s
snak-app-deployment-bc5b49548-m6nvx   1/1     Running   5 (5m30s ago)   7m6s
```
Є питання по тегах. Коли використовуємо якийсь чужий чарт (як от редіс від бітнамі)
```yaml
image:
    tag: "latest"
```
Бо я подивився які в них теги там є, то є latest, а решта хеші. Типу, що якщо мені потрібно редіс 7-alpine,
який використовувався в попередніх завданнях? Єдиний варіант сподіватися на те, що дозволять заоверрайдити якийсь параметр?

Ну інший прекол. Я поміняв той тег і спробував заранити
```
helm upgrade my-snak-app
```
чи
```
helm dependency update
```
Як я зрозумів, то депенденці апдейт тільки на депенденці в Chart.yaml працює. Інша команда не апгрейдила існуючі редіс ресурси.
Типу він всерівно намагався спулити старий імедж. Допомогло лише
```
helm uninstall my-snak-app && helm install my-snak-app .
```
Я пробував і
```
k rollout restart sts my-snak-app-redis-master
```
і
```
helm upgrade --force my-snak-app .
```
Пробував і версії чарту/апки міняти в Chart.yaml
Є якийсь інший спосіб змушувати ресурси перестворюватися зі змінами?
Конкретні ресурси, як от редіса в цьому випадку
