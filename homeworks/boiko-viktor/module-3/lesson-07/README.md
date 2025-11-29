
## Створення Namespace

створюємо namespace:
```bash
kubectl apply -f namespace.yml
```

## Деплой ресурсів

Застосуємо всі конфігураційні файли (ConfigMap, Deployment, Service):
```bash
kubectl apply -f .
```
# Deployment Strategies in Kubernetes
## RollingUpdate (Default)
### Конфігурація:
```yaml
spec:
  strategy:
    type: RollingUpdate
    rollingUpdate:
      maxSurge: 25%
      maxUnavailable: 20%
```
Це стратегія за замовчуванням. Вона дозволяє оновлювати Deployment без простою (типу zero downtime). Kubernetes поступово замінює старі поди на нові.

### Параметри:
- **maxSurge**: Максимальна кількість подів, які можуть бути створені *понад* бажану кількість реплік під час оновлення.
  - Може бути числом (наприклад, `2`) або відсотком (наприклад, `25%`).
  - *Приклад*: Якщо `replicas: 10` і `maxSurge: 2`, то під час оновлення може бути до 12 подів одночасно (10 старих + 2 нових). 
- **maxUnavailable**: Максимальна кількість подів, які можуть бути недоступні під час оновлення.
  - Може бути числом або відсотком.
  - *Приклад*: Якщо `replicas: 10` і `maxUnavailable: 2`, то мінімум 8 подів будуть завжди доступні (Ready).

### Переваги:
- **Zero Downtime**: Додаток завжди доступний для користувачів.
- **Контроль швидкості**: Можна налаштувати, як швидко оновлюється кластер.

### Недоліки:
- **Дві версії одночасно**: Під час оновлення працюють і стара, і нова версії додатку. Це може викликати проблеми, якщо вони використовують спільну базу даних зі зміненою схемою.

---

## Recreate

Ця стратегія спочатку видаляє **всі** старі поди, і тільки потім починає створювати нові.

### Конфігурація:
```yaml
spec:
  strategy:
    type: Recreate
```

### Переваги:
- **Чистий стан**: Ніколи не працюють дві версії одночасно. Це корисно, якщо нова версія не сумісна зі старою (наприклад, несумісні зміни в БД).

### Недоліки:
- **Downtime**: Є період часу (поки старі видалились, а нові ще не запустились), коли додаток повністю недоступний.

---


### Зміна ConfigMap
Зміна значень у `ConfigMap` **не призводить** до автоматичного перезапуску подів. Поди читають змінні середовища лише при старті.
Щоб застосувати зміни ConfigMap, потрібно kubectl rollout restart deployment course-app-deployment -n course-app-devперезапустити Deployment:
```bash
kubectl rollout restart deployment course-app-deployment -n course-app-dev
```

### Оновлення образу (RollingUpdate)
внесення змін у `deployment.yml` міняємо тег з lesson-04 на lesson-07 і застосуємо зміни:
```bash
kubectl apply -f deployment.yml
```
ми побачимо, як нові поди створюються (Running), а старі видаляються (Terminating) згідно з налаштуваннями `maxSurge` та `maxUnavailable`.

```bash
kubectl get pods -n course-app-dev -w                                                                                                    ─╯
NAME                                     READY   STATUS              RESTARTS       AGE
course-app-deployment-66979f499c-7nrht   1/1     Running             0              2s
course-app-deployment-66979f499c-8mjf8   1/1     Running             0              2s
course-app-deployment-66979f499c-jswdb   0/1     ContainerCreating   0              1s
course-app-deployment-66979f499c-nmss2   0/1     ContainerCreating   0              1s
course-app-deployment-66979f499c-rcccz   0/1     ContainerCreating   0              1s
course-app-deployment-66979f499c-rwnzk   0/1     ContainerCreating   0              1s
course-app-deployment-66979f499c-tr5t6   1/1     Running             0              2s
course-app-deployment-66979f499c-wtjxc   0/1     ContainerCreating   0              2s
course-app-deployment-66979f499c-xrvr9   1/1     Running             0              2s
course-app-deployment-7bc876bd88-bssvm   0/1     Completed           0              60s
course-app-deployment-7bc876bd88-mb7vx   1/1     Terminating         0              60s
course-app-deployment-7bc876bd88-mfbtb   1/1     Running             0              59s
course-app-deployment-7bc876bd88-mtm4c   1/1     Running             0              58s
course-app-deployment-7bc876bd88-nqw4h   1/1     Running             0              58s
course-app-deployment-7bc876bd88-pqpl6   1/1     Running             0              58s
course-app-deployment-7bc876bd88-r8f2l   1/1     Terminating         0              60s
course-app-deployment-7bc876bd88-rkcp6   1/1     Terminating         0              60s
redis-deployment-5b5ccc7596-tqhxd        1/1     Running             1 (6h3m ago)   6h11m
course-app-deployment-7bc876bd88-mb7vx   0/1     Completed           0              60s
course-app-deployment-66979f499c-wtjxc   1/1     Running             0              2s
course-app-deployment-7bc876bd88-nqw4h   1/1     Terminating         0              58s
course-app-deployment-66979f499c-sgtkm   0/1     Pending             0              0s
course-app-deployment-7bc876bd88-nqw4h   1/1     Terminating         0              58s
course-app-deployment-66979f499c-sgtkm   0/1     Pending             0              0s
course-app-deployment-66979f499c-nmss2   1/1     Running             0              1s
course-app-deployment-66979f499c-sgtkm   0/1     ContainerCreating   0              0s
course-app-deployment-66979f499c-rcccz   1/1     Running             0              1s
course-app-deployment-7bc876bd88-r8f2l   0/1     Completed           0              60s
course-app-deployment-7bc876bd88-pqpl6   1/1     Terminating         0              58s
course-app-deployment-7bc876bd88-pqpl6   1/1     Terminating         0              58s
course-app-deployment-7bc876bd88-mtm4c   1/1     Terminating         0              58s
course-app-deployment-7bc876bd88-mb7vx   0/1     Completed           0              60s
course-app-deployment-7bc876bd88-mb7vx   0/1     Completed           0              60s
course-app-deployment-7bc876bd88-rkcp6   0/1     Completed           0              60s
course-app-deployment-66979f499c-rwnzk   1/1     Running             0              1s
course-app-deployment-7bc876bd88-mtm4c   1/1     Terminating         0              58s
course-app-deployment-7bc876bd88-mfbtb   1/1     Terminating         0              59s
course-app-deployment-7bc876bd88-mfbtb   1/1     Terminating         0              59s
course-app-deployment-7bc876bd88-mfbtb   0/1     Completed           0              60s
course-app-deployment-7bc876bd88-mtm4c   0/1     Completed           0              59s
course-app-deployment-7bc876bd88-pqpl6   0/1     Completed           0              59s
course-app-deployment-7bc876bd88-nqw4h   0/1     Completed           0              59s
course-app-deployment-66979f499c-jswdb   1/1     Running             0              2s
course-app-deployment-66979f499c-sgtkm   1/1     Running             0              1s
course-app-deployment-7bc876bd88-mfbtb   0/1     Completed           0              60s
course-app-deployment-7bc876bd88-mfbtb   0/1     Completed           0              60s
course-app-deployment-7bc876bd88-r8f2l   0/1     Completed           0              61s
course-app-deployment-7bc876bd88-r8f2l   0/1     Completed           0              61s
course-app-deployment-7bc876bd88-mtm4c   0/1     Completed           0              59s
course-app-deployment-7bc876bd88-mtm4c   0/1     Completed           0              59s
course-app-deployment-7bc876bd88-nqw4h   0/1     Completed           0              59s
course-app-deployment-7bc876bd88-nqw4h   0/1     Completed           0              59s
course-app-deployment-7bc876bd88-bssvm   0/1     Completed           0              61s
course-app-deployment-7bc876bd88-bssvm   0/1     Completed           0              61s
course-app-deployment-7bc876bd88-bssvm   0/1     Completed           0              61s
course-app-deployment-7bc876bd88-rkcp6   0/1     Completed           0              61s
course-app-deployment-7bc876bd88-rkcp6   0/1     Completed           0              61s
course-app-deployment-7bc876bd88-pqpl6   0/1     Completed           0              59s
course-app-deployment-7bc876bd88-pqpl6   0/1     Completed           0              59s
```

## Очищення ресурсів

видаляємо ресурси:
```bash
kubectl delete -f .
```