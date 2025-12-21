#### Run 10 `nginx` containers
```
docker compose up --scale nginx=10 -d
```
#### Delete only `nginx`-related containers
```
docker rm -f $(docker ps -aq --filter ancestor=nginx)
```
