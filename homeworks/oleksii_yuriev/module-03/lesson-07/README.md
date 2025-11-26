# Simple App 🐳


## Create CM
```bash
cat cm.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: course-app-config
data:
  APP_MESSAGE: "Hello World"
  APP_STORE: "redis"

```

## Create Secret
```bash
cat secret.yml
apiVersion: v1
kind: Secret
metadata:
  name: redis-secret
type: Opaque
stringData:
  APP_REDIS_URL: "redis://:password@redis:6379/0"

```
## Get Secret & Decode 
```bash
kubectl get secret redis-secret -o yaml
apiVersion: v1
data:
  APP_REDIS_URL: cmVkaXM6Ly86cGFzc3dvcmRAcmVkaXM6NjM3OS8w
kind: Secret
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"v1","kind":"Secret","metadata":{"annotations":{},"name":"redis-secret","namespace":"default"},"stringData":{"APP_REDIS_URL":"redis://:password@redis:6379/0"},"type":"Opaque"}
  creationTimestamp: "2025-11-20T11:51:20Z"
  name: redis-secret
  namespace: default
  resourceVersion: "3165"
  uid: 2323209b-f62e-44a3-8362-5c06a3b631d9
type: Opaque

echo cmVkaXM6Ly86cGFzc3dvcmRAcmVkaXM6NjM3OS8w | base64 -d
redis://:password@redis:6379/0%

```
## Describe CM
```bash
kubectl describe  cm course-app-config
Name:         course-app-config
Namespace:    default
Labels:       <none>
Annotations:  <none>

Data
====
APP_MESSAGE:
----
Hello from ConfigMap

APP_STORE:
----
redis


BinaryData
====

Events:  <none>
```



##Deploy Deployment using CM & Secret
```bash
kubectl apply -f deployment_app.yml
```

## Verify environment variables in Pod
```bash
kubectl exec -it app-5cdbb4ccfb-qj5ww  -- env | egrep -i "APP_REDIS_URL|APP_STORE"
APP_STORE=redis
APP_REDIS_URL=redis://:password@redis:6379/0

```


## Rollout status/history/restart
kubectl rollout status deployment.apps/app                                                         
deployment "app" successfully rolled out

kubectl rollout history deployment.apps/app
deployment.apps/app
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>

kubectl rollout restart  deployment.apps/app
deployment.apps/app restarted

kubectl rollout history deployment.apps/app
deployment.apps/app
REVISION  CHANGE-CAUSE
1         <none>
2         <none>
3         <none>
4         <none>


```

## Check App
```bash
curl localhost:30080/healthz
{"status":"ok"}%

```
