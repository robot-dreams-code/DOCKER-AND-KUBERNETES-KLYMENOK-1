============================================
     README — Lesson 12
============================================

Homework — Module 04 / Lesson 12
Dragonfly Operator · Custom Resources · RBAC

Цей репозиторій містить артефакти для розгортання Dragonfly (Redis-compatible store) за допомогою Kubernetes Operator, підключення додатку course-app до Dragonfly та налаштування RBAC для доступу до кастомних ресурсів.

Структура репозиторію
lesson-12/
│
├── dragonfly.yaml            # Маніфест CR (Custom Resource) для розгортання Dragonfly
├── rbac.yaml                 # ServiceAccount, Role, RoleBinding для доступу до CR
├── course-app-deployment.yaml  # Deployment + Service для тестового застосунку
└── README.md

1. Встановлення Dragonfly Operator

Оператор встановлюється через офіційний Helm-чарт:

git clone https://github.com/dragonflydb/dragonfly-operator.git
cd dragonfly-operator

helm install dragonfly-operator charts/dragonfly-operator --namespace dragonfly-operator-system --create-namespace

Перевірка наявності CRD:

kubectl api-resources | findstr /I dragonfly

ресурс:
dragonflies      dragonflydb.io/v1alpha1          true         Dragonfly

2. Розгортання Dragonfly (Custom Resource)

Файл: dragonfly.yaml

Застосування:

kubectl apply -f dragonfly.yaml


Перевірка:

kubectl get dragonfly
*NAME               AGE
*dragonfly-sample   8s

kubectl get dragonflies
*NAME               AGE
*dragonfly-sample   67s

kubectl get pods -l app.kubernetes.io/name=dragonfly -n default
*NAME                 READY   STATUS    RESTARTS   AGE
*dragonfly-sample-0   1/1     Running   0          89s

kubectl get svc -n default | findstr /I dragonfly
*dragonfly-sample   ClusterIP   10.43.83.229   <none>     6379/TCP   117s
Сервіс Dragonfly доступний на порту 6379.

3. Розгортання course-app та підключення до Dragonfly

Файл: course-app-deployment.yaml

У Deployment використано змінні оточення:

REDIS_HOST=dragonfly-sample.default
REDIS_PORT=6379


Застосування:

або редагуємо YAML та виконуємо

kubectl apply -f course-app-deployment.yaml

можливо робити зміни через команду 
kubectl set env deployment/course-app REDIS_HOST=dragonfly-sample.default REDIS_PORT=6379 -n default

Перевірка:

kubectl get pods -n default
*NAME                         READY   STATUS    RESTARTS   AGE
*course-app-5dd944b46-kvh75   1/1     Running   0          54s
*dragonfly-sample-0           1/1     Running   0          5m48s

kubectl describe deploy course-app -n default | findstr /I REDIS
*REDIS_HOST:  dragonfly-sample.default
*REDIS_PORT:  6379

4. RBAC для Dragonfly Custom Resources

Файл: rbac.yaml створює:

ServiceAccount: db-viewer

Role: db-readonly

apiGroup: dragonflydb.io

resources: dragonflies, dragonflies/status

verbs: get, list, watch

RoleBinding: прив’язує SA до Role

Застосування:

kubectl apply -f rbac.yaml


Перевірка:

kubectl get sa db-viewer -n default
*NAME        SECRETS   AGE
*db-viewer   0         12s

kubectl get role db-readonly -n default
*NAME          CREATED AT
*db-readonly   2025-12-11T12:43:05Z

kubectl get rolebinding db-readonly-binding -n default
*NAME                  ROLE               AGE
*db-readonly-binding   Role/db-readonly   47s

5. Перевірка доступів (auth can-i)
kubectl auth can-i list dragonflies --as=system:serviceaccount:default:db-viewer
# yes

kubectl auth can-i delete dragonflies --as=system:serviceaccount:default:db-viewer
# no


RBAC налаштовано коректно: доступ тільки на читання.

6. Вимоги виконано

Dragonfly Operator встановлено

CRD створено

Dragonfly інстанс розгорнуто

course-app підключений до Dragonfly

Налаштовано ServiceAccount + Role + RoleBinding

Перевірено доступи через kubectl auth can-i