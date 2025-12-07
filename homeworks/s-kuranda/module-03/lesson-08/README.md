# robot_dreams :: Lessons-08

## Overview

Перевіряємо файл опису неймспейсу:
```bash
cat namespace.yml

apiVersion: v1
kind: Namespace
metadata:
  name: lesson-08
```

Створюємо наш окремий Namespace і змінюємо поточний контекст для зручності:
```bash
kubectl apply -f namespace.yml
kubectl config set-context --current --namespace=lesson-08
```

## Формування CM та Secret для нашого App
```bash
❯ kubectl apply -f configmap.yml
configmap/app-config created
❯ kubectl apply -f secret.yml
secret/app-secret created
```

## Безпосереднє опрацювання

Ініціюємо створення ресурсів

```bash
kubectl apply -f redis.deployment.yml
kubectl apply -f redis.svc.yml

kubectl apply -f app.deployment.yml
kubectl apply -f app.svc.yml
```

Перевіряємо готовність

```bash
❯ kubectl get deployments
NAME               READY   UP-TO-DATE   AVAILABLE   AGE
app-deployment     1/1     1            1           9s
redis-deployment   1/1     1            1           12m

❯ kubectl get pods
NAME                              READY   STATUS    RESTARTS   AGE
app-deployment-5d888b896b-cwwvt   1/1     Running   0          14s
redis-deployment-cbcf9cbb-m62xp   1/1     Running   0          3m6s
```

## Імплементація Ingress

### Формування SSL-сертифікату

Сертифікат будемо формувати через mkcert:

```bash
> brew install mkcert
✔︎ JSON API cask.jws.json                                                                                                            [Downloaded   15.0MB/ 15.0MB]
✔︎ JSON API formula.jws.json            [Downloaded   31.7MB/ 31.7MB]
==> Fetching downloads for: mkcert
✔︎ Bottle Manifest mkcert (1.4.4)       [Downloaded   13.2KB/ 13.2KB]
✔︎ Bottle mkcert (1.4.4)                [Downloaded    1.9MB/  1.9MB]
==> Pouring mkcert--1.4.4.arm64_tahoe.bottle.tar.gz
🍺  /opt/homebrew/Cellar/mkcert/1.4.4: 7 files, 4.5MB
==> Running `brew cleanup mkcert`...
```

Формуємо і інтегруємо в систему locally-trusted CA-сертифікат

```bash
❯ mkcert --install
Created a new local CA 💥
Sudo password:
The local CA is now installed in the system trust store! ⚡️
```

Формуємо сертифікат для домену `course-app.local` і його wildcard-варіації `*.course-app.local`

```bash
❯ mkdir cert && \
  mkcert -key-file cert/key.pem -cert-file cert/cert.pem course-app.local "*.course-app.local"

Created a new certificate valid for the following names 📜
 - "course-app.local"
 - "*.course-app.local"

Reminder: X.509 wildcards only go one level deep, so this won't match a.b.course-app.local ℹ️

The certificate is at "cert/cert.pem" and the key at "cert/key.pem" ✅
```

### Формування Secret для нашого Ingress
```bash
kubectl create secret tls ingress-tls --cert=cert/cert.pem  --key=cert/key.pem

kubectl get secret
NAME          TYPE                DATA   AGE
ingress-tls   kubernetes.io/tls   2      4s
```

### Безпосередній запйск Ingress

Ініціюємо створення ресурсів

```bash
❯ kubectl apply -f ingress.yml
ingress.networking.k8s.io/traefik-ingress created

❯ kubectl get ingress
NAME              CLASS     HOSTS                 ADDRESS        PORTS     AGE
traefik-ingress   traefik   a8.course-app.local   192.168.64.2   80, 443   8s

❯ kubectl describe ingress
Name:             traefik-ingress
Labels:           <none>
Namespace:        lesson-08
Address:          192.168.64.2
Ingress Class:    traefik
Default backend:  <default>
TLS:
  ingress-tls terminates course-app.local
Rules:
  Host                 Path  Backends
  ----                 ----  --------
  a8.course-app.local
                       /   app-svc:8080 (10.42.0.74:8080) <-- бачимо, що сервіс закріплений за доменом
Annotations:           traefik.ingress.kubernetes.io/rewrite-target: /
                       traefik.ingress.kubernetes.io/router.entrypoints: websecure
Events:                <none>
```

### Корегування сервісу

Для того, щоб інгресс-контроллер взяв на себе роль маршрутизації - потрібно скорегувати сервіс App під це. Загалом, навіть якщо не змінювати це - воно буде працювати, так як внутрішня маршрутизація в нас не змінилася і ми лише коректно "закриваємо" сервіс всередині кластеру...

```yaml
apiVersion: v1
kind: Service
metadata:
  name: app-svc
  namespace: lesson-08
spec:
  selector:
    app: app
  type: ClusterIP <-- тут змінили NodePort на ClusterIP
  ports:
    - name: app
      port: 8080
      targetPort: 8080
      #nodePort: 30088 <-- прибрали змінну nodePort
```

Приймаємо зміни і спостерігаємо за результатом:

```bash
❯ kubectl apply -f app.svc.yml
ingress.networking.k8s.io/traefik-ingress created

# ДО змін
❯ kubectl describe service app-svc
Name:                     app-svc
Namespace:                lesson-08
Labels:                   <none>
Annotations:              <none>
Selector:                 app=app
Type:                     NodePort
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.43.11.86
IPs:                      10.43.11.86
Port:                     app  8080/TCP
TargetPort:               8080/TCP
NodePort:                 app  30088/TCP
Endpoints:                10.42.0.74:8080
Session Affinity:         None
External Traffic Policy:  Cluster
Internal Traffic Policy:  Cluster
Events:                   <none>

# Після змін
❯ kubectl describe service app-svc
Name:                     app-svc
Namespace:                lesson-08
Labels:                   <none>
Annotations:              <none>
Selector:                 app=app
Type:                     ClusterIP
IP Family Policy:         SingleStack
IP Families:              IPv4
IP:                       10.43.11.86
IPs:                      10.43.11.86
Port:                     app  8080/TCP
TargetPort:               8080/TCP
Endpoints:                10.42.0.74:8080
Session Affinity:         None
Internal Traffic Policy:  Cluster
Events:                   <none>
```

І тепер можна перевірити сприйняття мультиподового виконання, коли в нас інгресс буде як точка входу для запитів на інші поди нашого сервісу. Для цього зробимо скейл і подивимося як всередині інгресс буде сприйматися ці зміни:

```bash
❯ kubectl describe ingress
Name:             traefik-ingress
...
...
Rules:
  Host                 Path  Backends
  ----                 ----  --------
  a8.course-app.local
                       /   app-svc:8080 (10.42.0.74:8080,10.42.0.80:8080,10.42.0.79:8080)
Annotations:           traefik.ingress.kubernetes.io/rewrite-target: /
                       traefik.ingress.kubernetes.io/router.entrypoints: websecure
Events:                <none>
```

## Хелсчекерство

Додамо до Deployment стратегії перевірки livenessProbe та readinessProb — механізми моніторингу здоров'я контейнерів усередині пода.

LivenessProbe - виявляє, коли контейнер "застряг" у зламаному стані (наприклад, deadlock, зависання). Якщо проба фейлиться, Kubernetes перезапускає контейнер.

ReadinessProbe - виявляє, чи готовий контейнер приймати трафік. Якщо фейлиться, под виключається з балансування навантаження (Service), але контейнер не перезапускається.

> Liveness — це "чи живий контейнер?" (якщо ні — рестарт). Readiness — це "чи готовий приймати запити?" (якщо ні — ізолювати від трафіку).

```yaml
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8080
            initialDelaySeconds: 5 <-- перший чекап - через 5 секунд після створення пода
            periodSeconds: 5 <-- період перевірки
            failureThreshold: 3 <-- кількість фейл-статусів
          livenessProbe:
            httpGet:
              path: /readyz
              port: 8080
            initialDelaySeconds: 15 <-- перший чекап - через 15 секунд після запуску
            periodSeconds: 10 <-- перевірка раз в 10 секунд
            failureThreshold: 3 <-- 3 спроби - перемикаємо у фейл
```

І от, стосовно, пунктів:
> - Перезапустити контейнер, якщо застосунок "завис"
> - Припинити надсилати трафік на под, якщо застосунок ще не завантажився або тимчасово не готовий до роботи

То тут за допомогою LivenessProbe ми покриємо перший пункт, а за допомогою ReadinessProbe - другий :)

Змусити наш деплойиент точково перевести readinessProbe у фейл можна було б через `kubectl patch` - це дозволило б динамічно оновити конфігурацію readinessProbe конкретного пода без рестарту контейнера чи зміни коду Deployment/додатка. Kubernetes підтримує патчинг probes в running подах — kubelet одразу застосовує нову конфігурацію для наступних перевірок (після periodSeconds). Це ідеально для тестування, бо ми не торкаємося коду застосунку, а просто "ламаємо" probe локально для одного пода:

```bash
> kubectl patch pod app-deployment-6658d898b9-wwnng --type='json' -p='[{"op": "replace", "path": "/spec/containers/0/readinessProbe/httpGet/path", "value": "/wrong-readyz"}]'

# отримуємо помилку:
The Pod "app-deployment-6658d898b9-wwnng" is invalid: spec: Forbidden: pod updates may not change fields other than `spec.containers[*].image`,`spec.initContainers[*].image`,`spec.activeDeadlineSeconds`,`spec.tolerations` (only additions to existing tolerations),`spec.terminationGracePeriodSeconds` (allow it to be set to 1 if it was previously negative)
```

Тобто по факту так просто обійти систему не вийде ((

Офіційно дозволені тільки вузькі зміни: image контейнерів, activeDeadlineSeconds, додавання tolerations та terminationGracePeriodSeconds. Probes (liveness/readiness/startup) не входять у цей список — їх не можна патчити на running поді без рестарту (а рестарт через patch image викличе перезапуск, що ми не хочемо для симуляції NotReady без рестарту).

То ж можна опрацювати цей формат через альтернативний формат readinessProbe - перевірку наявності відповідного файлу в системі (який ми можемо створити через init-контейнер) і вже точково видаливши файл всередині одного контейнеру - побачити спрацювання readinessProbe.

Щось на кшталт такого формату:

```yaml
        ...
        readinessProbe:
          exec:  # Exec probe: перевіряє файл /tmp/ready
            command:
            - cat
            - /tmp/ready
          initialDelaySeconds: 5
          periodSeconds: 5
          failureThreshold: 3
        livenessProbe:  # Простий, щоб не рестартувати
          exec:
            command:
            - cat
            - /tmp/healthy
          initialDelaySeconds: 15
          periodSeconds: 10
          failureThreshold: 3
      ...
      initContainers:  # Створює файли на старті
      - name: init-files
        image: busybox:1.35
        command: ["/bin/sh", "-c"]
        args:
        - |
          echo "healthy" > /tmp/healthy;
          echo "ready" > /tmp/ready;
        volumeMounts:
        - name: shared-volume
          mountPath: /tmp
```