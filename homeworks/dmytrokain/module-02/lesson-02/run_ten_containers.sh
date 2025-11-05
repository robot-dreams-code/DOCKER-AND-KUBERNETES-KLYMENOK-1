#!/bin/sh

for i in $(seq 1 10); do
  docker run -d --name nginx_container_$i nginx
done

