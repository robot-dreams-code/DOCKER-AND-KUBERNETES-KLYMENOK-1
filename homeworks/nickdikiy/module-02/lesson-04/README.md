## 1. Створимо Dockerfile та docker-compose.yaml
### Так як код додатку знаходиться в іншій директорії нам потрібно вказати правильні шляхи до контексту і докер файла.

## 2. Піднімемо контейнер:
```bash
docker compose up -d
```

## 3. Переконаємось що додаток працює, перейшовши на http://localhost:8080/

#### Бачимо що docker compose прокинув змінні середовища в додаток.
#### Відправимо кілька повідомлень, використовуючи UI інтерфейс.


## 4. Перевіримо що дані зберігаються в redis:
```bash
dokcer exec -it $(docker ps -aqf name="redis" | head -n 1) redis-cli
```

```bash
KEYS *
HGETALL message:1
```
```
1) "messages:seq"
2) "counters:visits"
3) "messages:ids"
4) "message:1"

1) "id"
2) "1"
3) "text"
4) "test message from UI stored in radis"
5) "created_at"
6) "2025-11-08T12:28:59.492625"
```
