# Run commands from homework directory
- `cd homeworks/zinkevych/module-02/lesson-05/`

# Run docker-compose.yaml
- `docker compose up`

# See redis logs
- `docker compose logs -f redis`

# See redis pings
- `docker inspect redis-server --format='{{json .State.Health}}' | python3 -m json.tool`

# Docker swarm
- `docker swarm init --advertise-addr <IP_ADDRESS>`
- build image from root: `docker build -t course-app -f homeworks/zinkevych/module-02/lesson-05/Dockerfile .`
- `docker stack deploy -c docker-compose-swarm.yaml course-app`
- check services: `docker stack ls`
- check services: `docker stack services course-app`


