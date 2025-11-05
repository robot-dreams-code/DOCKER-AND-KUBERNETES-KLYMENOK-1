## Build image
```bash
docker build -t simple-app \
  -f homeworks/klymenko-oleksandr/module-2/lesson-03/Dockerfile \
  apps/simple-app
```

## Run container
```bash
docker run --rm -p 8080:8080 simple-app
```

## Check
- http://localhost:8080
