# ConfigMap Integration and Deployment Update Write-Up

### Create and Apply ConfigMap

Define the configuration as a ConfigMap YAML and apply it to the cluster:

```bash
kubectl apply -f cm.yaml
```

Check the ConfigMap content and metadata:

```bash
kubectl get configmap course-app-config -n course-app-ns -o yaml
```

### Attach ConfigMap to Deployment

Reference the ConfigMap keys as environment variables in the `deployment.yaml` under container specs:

Reapply the manifests:

```bash
kubectl apply -f .
```

### Apply ConfigMap Changes to Pods

ConfigMap updates don’t automatically propagate. Restart Pods to pick up changes and monitor rollout:

```bash
kubectl rollout restart deployment/course-app -n course-app-ns
kubectl get pods -n course-app-ns -w
```

Verify environment variables are set in Pods:

```bash
kubectl describe pod <pod-name> -n course-app-ns | grep Environment -A2

# Example output:
#    Environment:
#      APP_ENV:    <set to the key 'APP_ENV' of config map 'course-app-config-map'>    Optional: false
#      LOG_LEVEL:  <set to the key 'LOG_LEVEL' of config map 'course-app-config-map'>  Optional: false
```

### Update Container Image and Rollout

Tag and push new image version:

```bash
docker tag holymykolay/course-app:latest holymykolay/course-app:0.1
docker push holymykolay/course-app:0.1
```

Update deployment image and apply:

```bash
# Update image in deployment.yaml to holymykolay/course-app:0.1
kubectl apply -f deployment.yaml
kubectl rollout status deployment/course-app -n course-app-ns
```

Confirm pods use new image:

```bash
kubectl get pods -n course-app-ns -o jsonpath="{.items[*].spec.containers[*].image}"

# Example output:
# holymykolay/course-app:0.1
```

### Explore Deployment Update Strategies

- **RollingUpdate (default):** Gradually updates pods with zero downtime by configuring `maxUnavailable` and `maxSurge`.
- **Recreate:** Stops all pods before creating new ones, causing downtime but simpler updates.

Define RollingUpdate strategy config in `deployment.yaml`:

```yaml
strategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 1
    maxSurge: 2
```

Apply and monitor rollout:

```bash
kubectl apply -f deployment.yaml
kubectl rollout status deployment/course-app -n course-app-ns
```

Switch to Recreate and observe the behavior:

```bash
# change strategy.type to Recreate in deployment.yaml
kubectl apply -f deployment.yaml
kubectl rollout status deployment/course-app -n course-app-ns
```

### Summary of Strategies

| Strategy      | Pros                          | Cons                       |
|---------------|-------------------------------|----------------------------|
| RollingUpdate | Zero downtime, safe rollouts  | Slower, uses more resources |
| Recreate      | Simpler, fast cutover         | Causes downtime            |
