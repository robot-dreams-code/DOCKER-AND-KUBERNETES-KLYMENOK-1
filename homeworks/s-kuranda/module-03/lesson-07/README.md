# robot_dreams :: Lessons-07

## Overview

Перевіряємо файл опису неймспейсу:
```bash
cat namespace.yml

apiVersion: v1
kind: Namespace
metadata:
  name: lesson-07
```

Створюємо наш окремий Namespace і змінюємо поточний контекст для зручності:
```bash
kubectl apply -f namespace.yml
kubectl config set-context --current --namespace=lesson-07
```

Враховуючи що в нашому поточному завданні ми використовуємо додаткові класи (ConfigMap, Secret, додаткові параметри...) - їх треба правильно прописати у вигляді додаткових файлів і параметрів.

<details>
    <summary>configmap.yml</summary>

    ```yaml
    apiVersion: v1
    kind: ConfigMap
    metadata:
    name: app-config
    namespace: lesson-07
    data:
    APP_TZ: "Europe/Kiev"
    APP_LANG: "en_US.UTF-8"
    APP_LC_ALL: "en_US.UTF-8"
    APP_LANGUAGE: "en_US:en"
    APP_MESSAGE: "Robot Dreams - Lesson 07 - MOD 1"
    APP_STORE: "redis"
    ```
</details>

<details>
    <summary>secret.yml</summary>

    ```yaml
    apiVersion: v1
    kind: Secret
    metadata:
    name: app-secret
    namespace: lesson-08
    type: Opaque
    stringData:
    APP_REDIS_URL: "redis://redis-svc:6379/0"
    ```
</details>

<br/>

Ну і, безпосередньо, імплементація нових класів у наших маніфестах розгортання:

<details>
    <summary>app.deployment.yml</summary>

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: app-deployment
  namespace: lesson-07
spec:
  replicas: 10
  ...
  spec:
    containers:
      - name: course-app
      image: kusandr0/robot_dreams_app:07-alpine-mod
      ports:
        - containerPort: 8080
      env:
        # Використовуємо значення змінних напряму з ConfigMap та Secret
        - name: TZ
          valueFrom:
            configMapKeyRef:
            name: app-config
            key: APP_TZ
        - name: LANG
          valueFrom:
            configMapKeyRef:
            name: app-config
            key: APP_LANG
        - name: LC_ALL
          valueFrom:
            configMapKeyRef:
            name: app-config
            key: APP_LC_ALL
        - name: LANGUAGE
          valueFrom:
            configMapKeyRef:
            name: app-config
            key: APP_LANGUAGE
        - name: APP_MESSAGE
          valueFrom:
            configMapKeyRef:
            name: app-config
            key: APP_MESSAGE
        - name: APP_STORE
          valueFrom:
            configMapKeyRef:
            name: app-config
            key: APP_STORE
        - name: APP_REDIS_URL
          valueFrom:
            secretKeyRef:
            name: app-secret
            key: APP_REDIS_URL

# Опис стратегії оновлення
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxSurge: 25%
    maxUnavailable: 25%
```
</details>

<br/>

Конфігурація `redis.deployment.yml` - за таким самим принципом (окрім Rolling Strategy)

## Безпосереднє опрацювання

Ініціюємо створенна ресурсів типу Deployment

```bash
kubectl apply -f configmap.yml
kubectl apply -f secret.yml

kubectl apply -f redis.deployment.yml
kubectl apply -f redis.svc.yml

kubectl apply -f app.deployment.yml
kubectl apply -f app.svc.yml
```

<details>
    <summary>Огляд новинов в нашому неймспейсі :)</summary>

### Деталізація по ConfigMap
```bash
❯ kubectl get cm -n lesson-07
NAME               DATA   AGE
app-config         6      7m17s
kube-root-ca.crt   1      7m24s

❯ kubectl describe cm -n lesson-07 app-config
Name:         app-config
Namespace:    lesson-07
Labels:       <none>
Annotations:  <none>

Data
====
APP_LANGUAGE:
----
en_US:en

APP_LC_ALL:
----
en_US.UTF-8

APP_MESSAGE:
----
Robot Dreams - Lesson 07

APP_STORE:
----
redis

APP_TZ:
----
Europe/Kiev

APP_LANG:
----
en_US.UTF-8


BinaryData
====

Events:  <none>
```

### Деталізація по Secret
```bash
❯ kubectl get secret -n lesson-07
NAME         TYPE     DATA   AGE
app-secret   Opaque   1      66m

❯ kubectl describe secret -n lesson-07 app-secret
Name:         app-secret
Namespace:    lesson-07
Labels:       <none>
Annotations:  <none>

Type:  Opaque

Data
====
APP_REDIS_URL:  24 bytes
```
</details>

## Опрацювання змін ConfigMap

Перед зміною ConfigMap - подивимося поточні значення всередині одного з подів:

```bash
kubectl exec -n lesson-07 app-deployment-695bb6d646-2bczq -- env

HOSTNAME=app-deployment-695bb6d646-2bczq
...
TZ=Europe/Kiev
LANG=en_US.UTF-8
LC_ALL=en_US.UTF-8
LANGUAGE=en_US:en
APP_MESSAGE=Robot Dreams - Lesson 07
APP_STORE=redis
APP_REDIS_URL=redis://redis-svc:6379/0
...
PYTHON_VERSION=3.14.0
PYTHON_SHA256=2299dae542d395ce3883aca00d3c910307cd68e0b2f7336098c8e7b7eee9f3e9
HOME=/home/appuser
```

Після зміни значення і повторного застосування (`kubectl apply ...`) - переглядаємо зміни:

```bash
kubectl exec -n lesson-07 app-deployment-f68665c8b-48vpl -- env

...
APP_MESSAGE=Robot Dreams - Lesson 07 - MOD 1
...
```

## Дослідження поведінки зміни стратегії розгортання

Враховуючи наявність двох стратегій розгортання (Recreate, RollingUpdate), які в свої основі мають різний функціональний результат ("повна заміна" проти "поступового оновлення", якщо дуже коротко) - зупинимося на останньому (RollingUpdate).

Зазначивши "бест практікс" значення maxSurge та maxUnavailable = 25% - можна побачити процес оновлення згідно документації:

```bash
kubectl apply -f app.deployment.yml

kubectl rollout restart -n lesson-07 deployment app-deployment

kubectl get pods -n lesson-07

NAME                               READY   STATUS              RESTARTS   AGE
app-deployment-75bb878567-4ntn9    1/1     Running             0          1s
app-deployment-75bb878567-67zr5    0/1     ContainerCreating   0          0s
app-deployment-75bb878567-jd7qk    1/1     Running             0          1s
app-deployment-75bb878567-jfphl    1/1     Running             0          1s
app-deployment-75bb878567-mm8st    0/1     ContainerCreating   0          0s
app-deployment-75bb878567-mmx4m    1/1     Running             0          1s
app-deployment-75bb878567-nwlfg    1/1     Running             0          1s
app-deployment-75bb878567-p5pqm    0/1     ContainerCreating   0          0s
app-deployment-f68665c8b-48vpl     1/1     Running             0          4m
app-deployment-f68665c8b-52hdd     1/1     Running             0          4m1s
app-deployment-f68665c8b-5xcb5     0/1     Completed           0          4m2s
app-deployment-f68665c8b-b2bfl     1/1     Running             0          4m2s
app-deployment-f68665c8b-hfpc2     1/1     Running             0          4m1s
app-deployment-f68665c8b-nnlkz     0/1     Completed           0          4m1s
app-deployment-f68665c8b-srxdf     1/1     Running             0          4m
app-deployment-f68665c8b-tmscw     0/1     Completed           0          4m2s
redis-deployment-ff4547df8-9cgz5   1/1     Running             0          12m
```

Вказуємо `maxUnavailable: 0` і `maxSurge: 5`

```bash
kubectl get pods -n lesson-07
NAME                               READY   STATUS              RESTARTS   AGE
app-deployment-6758768b4d-52mfj    1/1     Running             0          2m7s
app-deployment-6758768b4d-7frtf    1/1     Running             0          2m7s
app-deployment-6758768b4d-846xw    1/1     Running             0          2m7s
app-deployment-6758768b4d-cdfm6    1/1     Running             0          2m7s
app-deployment-6758768b4d-fht58    1/1     Running             0          2m7s
app-deployment-6758768b4d-j5m2l    1/1     Terminating         0          2m7s
app-deployment-6758768b4d-jlb7s    1/1     Terminating         0          2m7s
app-deployment-6758768b4d-n8vnt    1/1     Running             0          2m7s
app-deployment-6758768b4d-tkzx5    1/1     Terminating         0          2m7s
app-deployment-6758768b4d-wkwp7    1/1     Running             0          2m7s
app-deployment-7ffd8c65b6-4vs9k    1/1     Running             0          2s
app-deployment-7ffd8c65b6-fx9hk    1/1     Running             0          2s
app-deployment-7ffd8c65b6-gxfmg    1/1     Running             0          2s
app-deployment-7ffd8c65b6-k968j    0/1     ContainerCreating   0          1s
app-deployment-7ffd8c65b6-lgprv    0/1     ContainerCreating   0          1s
app-deployment-7ffd8c65b6-mxvkk    0/1     ContainerCreating   0          1s
app-deployment-7ffd8c65b6-tbkg2    1/1     Running             0          2s
app-deployment-7ffd8c65b6-vwnsg    1/1     Running             0          2s
redis-deployment-ff4547df8-9cgz5   1/1     Running             0          84m
```

В такому випадку ми не чіпаємо старі поди, а створюємо лише нові і поступово, враховуючи кількість реплік (10) і умову - залишаємо активними 10 подів в будь якому разі).

Спробуємо, з урахуванням поточних реплік `replicas: 10` вказати `maxUnavailable: 10` і `maxSurge: 5`

```bash
❯ kubectl get pods -n lesson-07
NAME                               READY   STATUS              RESTARTS   AGE
app-deployment-6f577856f7-2dkxz    0/1     ContainerCreating   0          1s
app-deployment-6f577856f7-6c5c4    0/1     ContainerCreating   0          2s
app-deployment-6f577856f7-d6twk    0/1     ContainerCreating   0          2s
app-deployment-6f577856f7-g92kg    0/1     ContainerCreating   0          2s
app-deployment-6f577856f7-gwj28    0/1     ContainerCreating   0          2s
app-deployment-6f577856f7-h2h9t    0/1     ContainerCreating   0          2s
app-deployment-6f577856f7-j8dgt    0/1     ContainerCreating   0          2s
app-deployment-6f577856f7-nzm4r    0/1     ContainerCreating   0          2s
app-deployment-6f577856f7-xmstw    0/1     ContainerCreating   0          1s
app-deployment-6f577856f7-z8hcs    0/1     ContainerCreating   0          2s
redis-deployment-ff4547df8-9cgz5   1/1     Running             0          91m

❯ kubectl get pods -n lesson-07
NAME                               READY   STATUS    RESTARTS   AGE
app-deployment-6f577856f7-2dkxz    1/1     Running   0          2s
app-deployment-6f577856f7-6c5c4    1/1     Running   0          3s
app-deployment-6f577856f7-d6twk    1/1     Running   0          3s
app-deployment-6f577856f7-g92kg    1/1     Running   0          3s
app-deployment-6f577856f7-gwj28    1/1     Running   0          3s
app-deployment-6f577856f7-h2h9t    1/1     Running   0          3s
app-deployment-6f577856f7-j8dgt    1/1     Running   0          3s
app-deployment-6f577856f7-nzm4r    1/1     Running   0          3s
app-deployment-6f577856f7-xmstw    1/1     Running   0          2s
app-deployment-6f577856f7-z8hcs    1/1     Running   0          3s
redis-deployment-ff4547df8-9cgz5   1/1     Running   0          91m
```

Видно, що "автоматика" врахувала наші умови і начисто створила 10 нових подів, не дивлячись на потребу в резервуванні активних сервісів для опрацювання запитів. Як би мовити "сам так зазначив" :)

> А по факту - отримали той самий Recreate але у вигляді RollingUpdate

Тому треба завжди уважно описувати подібні параметри, бо витримати SLA за таких умов буде неможливо :)