docker swarm init
docker build -t my-python-app:latest -f Dockerfile ../../../../
docker stack deploy -c docker-compose-swarm.yaml myapp