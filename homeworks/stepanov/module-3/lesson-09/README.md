k get sc повертає local-path (default), все ок

Спочатку завтикав і описав деплоймент для редіса, хоча треба було стейтфул сет)

Загалом, все получилося

k get pvc повертає наступне

```
NAME                 STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data-redis-0   Bound    pvc-0c718085-1776-4f69-b45d-e8de63e60953   1Gi        RWO            local-path     <unset>                 59s
```

Далі я зайшов в редіс

```
kubectl exec -it redis-0 -- redis-cli
```
І засетив значення
```
SET testkey "Hello from Redis"
GET testkey
exit
```
Після цього я дропнув под
```
kubectl delete pod redis-0
```

Кубер його підняв і я знову зайшов в редіс затестити, чи зберігся ключ
```
kubectl exec -it redis-0 -- redis-cli
GET testkey
exit
```

Все збереглося. На UI теж все збереглося
