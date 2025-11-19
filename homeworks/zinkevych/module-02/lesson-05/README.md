# Run commands from homework directory
- `cd homeworks/zinkevych/module-02/lesson-05/`

# Run docker-compose.yaml
- `docker compose up`

# See redis logs
- `docker compose logs -f redis`

# See redis pings
- `docker inspect redis-server --format='{{json .State.Health}}' | python3 -m json.tool`


