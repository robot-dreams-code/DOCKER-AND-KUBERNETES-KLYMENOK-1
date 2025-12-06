# homework-11

Створення чарту `helm create course-app`

Перегляд маніфестів
`helm template course-app --debug`

Створення неймспейсу і встановлення чарту
`kubectl create namespace course-app-dev`

`helm upgrade --install course-app ./course-app -n course-app-dev`

Додаємо Redis

`helm repo add bitnami https://charts.bitnami.com/bitnami`
`helm upgrade --install redis bitnami/redis -n course-app-dev --set auth.enabled=false`

Перевірка Redis

```
kubectl exec --tty -i redis-master-0 --namespace course-app-dev -- bash

redis-cli
127.0.0.1:6379> SCAN 0
1) "0"
2) 1) "counters:visits"

GET counters:visits
127.0.0.1:6379> GET counters:visits
"11"
```

Ще перевіряємо по API  
```
kyrylich@Kyrylos-Laptop lesson-11 % curl https://course-app.local/api/info -Lk | jq
{
  "app": "course-app",
  "hostname": "course-app-5fcbc9b466-vnf6v",
  "store": "redis",
  "db_path": "data/data.sql",
  "redis_url": "redis://redis-master:6379",
  "messages_api": "",
  "counter_api": "",
  "message": "Welcome to the Course App",
  "secret_token_present": false,
  "env": {
    "APP_REDIS_URL": "redis://redis-master:6379",
    "APP_STORE": "redis"
  }
}
```
