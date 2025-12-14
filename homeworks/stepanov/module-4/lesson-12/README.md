```
k exec -it snak-app-dragonfly-instance-0 -- redis-cli
KEYS *
```
Повернуло:
```
KEYS *
1) "message:1"
2) "messages:ids"
3) "messages:seq"
4) "message:2"
5) "message:3"
6) "counters:visits"
```
Ну, стор не пустий, а значить драгонфлай працює.

Далі виконав 2 і 3 пункти. Все получилося

```
kubectl auth can-i list dragonflies --as=system:serviceaccount:robotdreams:db-viewer
yes
```
```
kubectl auth can-i delete dragonflies --as=system:serviceaccount:robotdreams:db-viewer
no
```
