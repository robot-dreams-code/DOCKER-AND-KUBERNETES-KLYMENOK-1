# Docker hub (Запушити зібраний імедж для apps/course-app у Docker Hub або GitHub Registry)

1. `docker login -u kyrops`
2. `docker build ../../../../apps/course-app -t kyrops/course-app -f ./Dockerfile`
3. `docker push kyrops/course-app`
4. Image of `course-app` is available here — https://hub.docker.com/r/kyrops/course-app


# K8S: Namespace | Deployment | Service

1. cd dev/
2. `kubectl apply -f ./app-namespace.yaml`
3. `kubectl apply -f ./app-deployment.yaml`
4. `kubectl apply -f ./app-service.yaml`

