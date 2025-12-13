Розбирався з хельмом разом з АІшкою. Суть уловив. 
```
k get pods
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

Воно скачує архівчик з редісом в папку проекту, це очікувано? Типу після 
```
helm dependency update
```
Воно скачує депенденці локально в charts/redis-18.0.0.tgs

Ще інше питання це теги. Коли використовуємо чиїсь чужі чарти (як от редіс) то в 90% випадків так має бути?
```yaml
image:
    tag: "latest"
```
Бо я подивився які в них теги там є, то є latest, а решта хеші. Типу, що якщо мені потрібно редіс alpine-7
