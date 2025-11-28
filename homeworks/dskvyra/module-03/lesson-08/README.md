# Service Discovery, Health Checks, Ingress, Zero Downtime Test Write-up

### Change Service Type to ClusterIP

Edit `service.yaml` to change the Service type from `NodePort` to `ClusterIP` for internal cluster communication and apply:

```bash
kubectl apply -f service.yaml
```

Verify Service:

```bash
kubectl get svc course-app-service -n course-app-ns
```

### Test Internal Connectivity

Run a debug pod inside the cluster namespace and test access to the Service:

```bash
kubectl run debug -it --rm --image=busybox --restart=Never -n course-app-ns -- sh
wget -qO- http://course-app-service:8080
```

### Health Checks

Add liveness and readiness probes to the Deployment in `deployment.yaml`:

```yaml
livenessProbe:
  httpGet:
    path: /healthz
    port: 8080
  initialDelaySeconds: 15
  periodSeconds: 20
  failureThreshold: 3
readinessProbe:
  httpGet:
    path: /readyz
    port: 8080
  initialDelaySeconds: 5
  periodSeconds: 10
  failureThreshold: 3
```

Apply updates:

```bash
kubectl apply -f deployment.yaml
```

Check Pod status and event logs:

```bash
kubectl describe pod <pod-name> -n course-app-ns
```

There shouldn't be any problems in Events and all Conditions should be true

Use a debug pod to verify app health endpoints if needed.

```bash
kubectl run debug -it --rm --image=busybox --restart=Never -n course-app-ns -- sh
wget -qO- http://course-app-service:8080/healthz
# {"status":"ok"}

wget -qO- http://course-app-service:8080/readyz
# {"status":"ready"}
```

### Ingress Setup

Create an Ingress resource in `ingress.yaml` to expose the app via hostname `course-app.local`:

Apply Ingress:

```bash
kubectl apply -f ingress.yaml
kubectl get ingress -n course-app-ns
```

Map hostname to ingress IP or locally for testing:

Add to `/etc/hosts`:

```
127.0.0.1 course-app.local
```

### Zero Downtime Testing

Simulate readiness probe failure in a Pod without stopping the container:

```bash
kubectl exec -it <pod-name> -n course-app-ns -- sh
kill 1  # Simulates app failure causing readiness probe to fail
```

Watch endpoints update (Pod IP removed due to readiness failure):

```bash
kubectl get pods -n course-app-ns -w
kubectl get endpoints course-app-service -n course-app-ns -o wide -w
```

Verify that the Pod IP disappears from the endpoints and that a new one is created shortly thereafter
