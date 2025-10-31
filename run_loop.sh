#!/bin/sh
for i in {1..10}; do
    PORT=$((8080 + i))
    docker run -dp ${PORT}:80 \
    -e INDEX="$i" \
    "$1"
done
