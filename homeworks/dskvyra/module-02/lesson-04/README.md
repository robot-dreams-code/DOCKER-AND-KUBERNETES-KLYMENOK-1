## Setup Instructions

Copy the `Dockerfile` and `docker-compose.yml` files into the root of the `apps/course-app` directory

## Running with Docker Compose

1. Build and start services:

- in the foreground
```
docker-compose up --build
```

- in deattached mode
```
docker-compose up --build -d
```

2. Access the app at: [http://localhost:8080](http://localhost:8080)

3. Stop the services:  
```
docker-compose down
```