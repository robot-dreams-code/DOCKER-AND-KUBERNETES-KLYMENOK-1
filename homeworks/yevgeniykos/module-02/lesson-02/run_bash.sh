for i in {0..9}; do
    HOST_PORT=$((8081 + $i))
    docker run -d --rm --name nginx-yevgeniy-$i -p $HOST_PORT:80 nginx:latest
done
