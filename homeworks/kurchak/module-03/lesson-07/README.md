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
kubectl apply -f k8s/configmap.yaml
```
#### To verify everything
```
kubectl get pods
kubectl get services
kubectl logs deployment/course-app
kubectl logs deployment/redis
```
#### After applying changes to configmap.yaml
```
kubectl apply -f k8s/configmap.yaml
kubectl rollout restart deployment/course-app
kubectl rollout status deployment/course-app
```
#### At the end, perform cleanup
```
kubectl delete -f k8s/course-app.yaml
kubectl delete -f k8s/redis.yaml
kubectl delete -f k8s/configmap.yaml
```

#### RollingUpdate tuning & Replace/Recreate strategy
| Strategy / Settings | Pros | Cons | Use when… |
| :-- | :-- | :-- | :-- |
| RollingUpdate (default) | Gradual updates, can keep service up | Slight traffic mix (old vs new) during rollout | Most stateless workloads |
| RollingUpdate (maxSurge >0, maxUnavailable 0) | Zero downtime if new pods become ready quickly | Requires capacity for extra pods | Highly sensitive to downtime |
| RollingUpdate (maxSurge 0, maxUnavailable >0) | Doesn’t require extra capacity | Can dip below desired replicas during rollout | Resource-constrained environments |
| Recreate/Replace | Guarantees only one version at a time | Full downtime | Apps needing shutdown of old version first |
