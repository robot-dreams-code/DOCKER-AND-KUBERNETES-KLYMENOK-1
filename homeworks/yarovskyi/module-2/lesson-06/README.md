# Lesson 06 Kubernetes Deployment and Service

1. Create a namespace:
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-06/namespace.yaml 
```

2. Switch namespace (kubens must be installed previously):
```bash
kubens robotdreams
```

3. Deploy Deployment:
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-06/deployment.yaml
```
Check deployment and pods in Workloads tab in Kubernetes Dashboard.

4. Deploy Service:
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-06/service.yaml
```
Check service in Service Discovery -> Services tab in Kubernetes Dashboard.
Check app by going to http://localhost:30080.

5. Change 'replicas' count in deployment.yaml and run again:
```bash
kubectl apply -f homeworks/yarovskyi/module-2/lesson-06/deployment.yaml
```
Check the pods number in the Workloads tab in Kubernetes Dashboard.

6. Stop/Delete Service and Deployment
```bash
kubectl delete -f homeworks/yarovskyi/module-2/lesson-06/service.yaml
kubectl delete -f homeworks/yarovskyi/module-2/lesson-06/deployment.yaml
```
Check that the service, deployment and pods are deleted in Kubernetes Dashboard.
