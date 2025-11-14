## 1. Перевикористаємо Dockerfile з попереднього уроку.

## 2. Змінимо docker-compose.yaml 
* Додаємо volume redis-data для збереження данних між перезапусками контейнерів.
* Додаємо healthcheck для перевірки готовності контейнера redis.
* command: [ "redis-server", "--appendonly", "yes" ] потрібен для того, щоб мати дамп редіса в ріал таймі.

## 2. Піднімемо контейнер та перевіримо що redis healthy:
```bash
docker compose up -d
docker ps
```
```
CONTAINER ID   IMAGE              COMMAND                  CREATED              STATUS                        PORTS                                         NAMES
77744cce0827   lesson-05-python   "uvicorn src.main:ap…"   About a minute ago   Up About a minute             0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp   lesson-05-python-1
60fd7a5746f1   redis:latest       "docker-entrypoint.s…"   About a minute ago   Up About a minute (healthy)   0.0.0.0:6379->6379/tcp, [::]:6379->6379/tcp   lesson-05-redis-1
```

## 3. Переконаємось що додаток працює, перейшовши на http://localhost:8080/. Відправимо кілька повідомлень.

## 4. Перевіримо що дані зберігаються в redis:
```bash
docker exec -it $(docker ps -aqf name="redis" | head -n 1) redis-cli
```

```bash
KEYS *
HGETALL message:2
```
```
1) "message:2"
2) "messages:seq"
3) "counters:visits"
4) "message:1"
5) "messages:ids"

1) "id"
2) "2"
3) "text"
4) "rty"
5) "created_at"
6) "2025-11-14T07:17:12.391143"
```
## 5. Перезапустимо контейнери та переконаємось що дані збережено.
```bash
docker compose down && docker compose up -d
docker exec -it $(docker ps -aqf name="redis" | head -n 1) redis-cli KEYS '*'
```
```
1) "message:1"
2) "messages:seq"
3) "messages:ids"
4) "counters:visits"
5) "message:2"
```
#### Можна використати і docker compose restart. Я використовую саме docker compose down && docker compose up -d, тому що це гарантує чистий перезапуск контейнерів з змінами з ямл файла. Також така комбінаціє "очистить" все крім іменнованого volume. Це дуже корисно, тому що в мене спочатку створювався анонімний volume і перезапуск за допомогою restart відображав дані. Тобто здавалось що все працює, але на справді створювався анонімний волюм. Причина була в тому що я не змінив директорію, і працював з файлами з lesson-04.
#### Щоб переконатись що volume налаштований коректно можна виконати docker inspect $(docker ps -aqf name="redis" | head -n 1) і переконатись що ми використовуємо іменований volume