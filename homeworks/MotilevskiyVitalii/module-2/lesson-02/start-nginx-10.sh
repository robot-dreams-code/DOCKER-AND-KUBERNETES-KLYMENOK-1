#!/usr/bin/env bash
set -euo pipefail

for i in $(seq 1 10); do
  docker run -d --name "nginx-$i" \
    -p $((8080+i)):80 \
    --restart unless-stopped \
    nginx:alpine
done