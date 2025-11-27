#### Publish 'course-app' image to Docker Hub:
```
docker build -t docker.io/<dockerhub-username>/course-app:1.0 .
docker login docker.io
docker push docker.io/<dockerhub-username>/course-app:1.0
```
#### Generate self-signed certificate
```
$hostName = "course-app.127.0.0.1.sslip.io"

#if required, only for Windows:
winget install --id ShiningLight.OpenSSL.Light -e

openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout tls.key -out tls.crt -subj "/CN=$hostName/O=CourseApp"

kubectl create secret tls course-app-tls --cert=tls.crt --key=tls.key
```
#### Apply the manifests
```
kubectl apply -f k8s/redis.yaml
kubectl apply -f k8s/course-app.yaml
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/course-app-ingress.yaml
```
#### To verify everything
```
kubectl get pods
kubectl get services
kubectl get ingress course-app
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
kubectl delete -f k8s/course-app-ingress.yml
```
#### Zero-downtime test (readiness failure)
| Step | Command | Expected Result / Notes |
| :-- | :-- | :-- |
| 1. Select a pod | ```POD=$(kubectl get pods -l app=course-app -o jsonpath='{.items[0].metadata.name}')<br>echo "$POD"``` | Saves the name of one replica (to target in later commands). |
| 2. Break its Redis connectivity (simulated failure) | ```kubectl exec --user root "$POD" -- sh -c "echo '127.0.0.1 redis' >> /etc/hosts"``` | Forces that pod to resolve redis to 127.0.0.1, so readiness probe (which depends on Redis) starts failing. The container keeps running. |
| 3. Watch readiness status | ```kubectl get pod "$POD" -w``` | After a few probe failures, the pod shows READY 0/1 but stays in Running. Kubernetes stops routing traffic to it. |
| 4. Inspect service endpoints | ```kubectl get endpoints course-app -o wide``` | IP of the failing pod disappears from the endpoints list. Only healthy replicas receive traffic, so no downtime for clients. |
| 5. Restore normal state | ```kubectl delete pod "$POD"``` | ReplicaSet replaces the pod. The new pod passes readiness probes, rejoins the endpoint list, and cluster returns to 10 healthy replicas. |