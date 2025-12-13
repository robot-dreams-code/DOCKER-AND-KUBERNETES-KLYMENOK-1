# Dragonfly Operator & RBAC

### Встановлення Dragonfly Operator


```bash
# Додаємо репозиторій
helm repo add dragonflydb https://dragonflydb.github.io/helm-charts
helm repo update
```

```bash
# Встановлення оператора в namespace 'dragonfly-system'
helm upgrade --install dragonfly-operator "oci://ghcr.io/dragonflydb/dragonfly-operator/helm/dragonfly-operator" \
  --version v1.3.1 \
  --namespace dragonfly-system \
  --create-namespace 
```

### Розгортання застосунку

```bash
# Встановлення чарту
helm upgrade --install course-app . \
  --namespace course-app-dev \
  --create-namespace \
  --set dragonflyOperator.enabled=false 
```

### Перевірка компонентів
**Оператор**:
   ```bash
   k get pods -n dragonfly-system
   NAME                                  READY   STATUS    RESTARTS   AGE
dragonfly-operator-7f9d4f5d8f-2rctv   2/2     Running   0          5m53s
   ```
**Застосунок та БД** (в робочому namespace):
   ```bash
   k get pods -n course-app-dev
   NAME                          READY   STATUS    RESTARTS   AGE
course-app-698c9d845b-vgr65   1/1     Running   0          40s
course-app-698c9d845b-w48rx   1/1     Running   0          16s
course-app-698c9d845b-wsnhd   1/1     Running   0          28s
dragonfly-course-app-0        1/1     Running   0          2m20s
   ```

### Перевірка логів застосунку
```bash
k logs -l app.kubernetes.io/name=course-app -n course-app-dev --tail=2
INFO:     10.42.0.1:49840 - "GET /healthz HTTP/1.1" 200 OK
INFO:     10.42.0.1:49846 - "GET /readyz HTTP/1.1" 200 OK
INFO:     10.42.0.1:36560 - "GET /healthz HTTP/1.1" 200 OK
INFO:     10.42.0.1:38588 - "GET /readyz HTTP/1.1" 200 OK
```

## Верифікація RBAC (ServiceAccount)
ServiceAccount `db-viewer` створюється в namespace `course-app-dev`.

```bash
# 1. Перевірка доступу на перегляд (Очікується: yes)
k auth can-i list dragonflies --as=system:serviceaccount:course-app-dev:db-viewer -n course-app-dev
yes
```

```bash
# 2. Перевірка заборони на видалення (Очікується: no)
k auth can-i delete dragonflies --as=system:serviceaccount:course-app-dev:db-viewer -n course-app-dev
no
```

## Видалення

```bash
# Видалення застосунку
helm uninstall course-app -n course-app-dev

# Видалення оператора
helm uninstall dragonfly-operator -n dragonfly-system
```
