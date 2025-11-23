## Running Locally

```
# Run directly:
go run main.go
# Or build and run:
go build -o app main.go
./app
```

## Running using Docker container

```
# Using command line, go to 'simple-app' directory:
cd /Users/your_user/IdeaProjects/DOCKER-AND-KUBERNETES-KLYMENOK-1/apps/simple-app
# In this directory, build image:
docker build -t simple-app:latest -f apps/simple-app/Dockerfile .
./app
# After that, run container: 
docker run -p 8080:8080 simple-app
```

## Visit http://localhost:8080

## Pushing your image to Docker Hub

```
# Login into Docker Hub:
docker login
# From working directory, push your image:
docker push imple-app:latest
# Run container from registry:
docker run -d -p 8080:8080 simple-app:latest
```