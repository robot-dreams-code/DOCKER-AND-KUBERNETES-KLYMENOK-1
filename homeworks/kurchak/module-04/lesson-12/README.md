#### Install Dragonfly Operator via Helm
```
helm repo add dragonfly-operator https://helm.dragonflydb.io
helm repo update
helm install dragonfly-operator dragonfly-operator/dragonfly-operator --namespace dragonfly-system --create-namespace
```
#### Verify CRDs
```
kubectl api-resources | grep dragonfly
```
#### Apply the manifests
```
kubectl apply -f k8s/dragonfly.yaml
kubectl apply -f k8s/dragonfly-rbac.yaml
kubectl get dragonfly
kubectl get pods -l app.kubernetes.io/name=dragonfly
kubectl get svc dragonfly-main
```
#### Verify RBAC
```
# Should return "yes"
kubectl auth can-i list dragonflies --as=system:serviceaccount:default:db-viewer

# Should return "no"
kubectl auth can-i delete dragonflies --as=system:serviceaccount:default:db-viewer
```
#### Uninstall Helm releases
```
helm uninstall course-app
helm uninstall redis
helm uninstall dragonfly-operator -n dragonfly-system
```
#### Verify cleanup
```
kubectl get all
kubectl get crd | grep dragonfly
kubectl get pvc
helm ls -A
```
#### Prune dangling volumes if necessary
```
kubectl delete pvc --all
```
