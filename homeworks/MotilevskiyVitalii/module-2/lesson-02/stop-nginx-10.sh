#!/usr/bin/env bash
set -euo pipefail

docker rm -f $(docker ps -qf "ancestor=nginx:alpine")