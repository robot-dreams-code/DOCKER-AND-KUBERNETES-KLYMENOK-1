#### Publish 'course-app' image to Docker Hub:
```
docker build -t docker.io/<dockerhub-username>/course-app:1.0 .
docker login docker.io
docker push docker.io/<dockerhub-username>/course-app:1.0
```
#### Apply the manifests
```
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/course-app.yaml
```
#### To verify everything
```
kubectl get pods
kubectl get services
kubectl logs deployment/course-app
kubectl logs deployment/redis
```
#### At the end, perform cleanup
```
kubectl delete -f k8s/course-app.yaml
kubectl delete -f k8s/redis.yaml
```
