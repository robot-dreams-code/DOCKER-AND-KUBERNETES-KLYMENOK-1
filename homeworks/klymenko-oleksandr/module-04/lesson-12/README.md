# Homework: Module 04 / Lesson 12

## 1. Dragonfly Operator
```bash
kubectl create namespace dragonfly-system --dry-run=client -o yaml | kubectl apply -f -
helm repo add jacobcolvin https://jacobcolvin.com/helm-charts
helm repo update
helm upgrade --install dragonfly-operator jacobcolvin/dragonfly-operator `
  -n dragonfly-system `
  --create-namespace `
  --version 0.1.1 `
  --set crds.install=true
kubectl api-resources | Select-String dragonfly
kubectl explain dragonfly.spec
```

## 2. Інстанс Dragonfly (CR)
```bash
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -f homeworks/klymenko-oleksandr/module-04/lesson-12/k8s/dragonfly.yaml
kubectl get dragonfly,sts,svc -n dev
```

## 3. RBAC
```bash
kubectl apply -f homeworks/klymenko-oleksandr/module-04/lesson-12/k8s/rbac.yaml
kubectl auth can-i list dragonflies --as=system:serviceaccount:default:db-viewer
kubectl auth can-i delete dragonflies --as=system:serviceaccount:default:db-viewer
```

## 4. course-app з Dragonfly
```bash
$env:DOCKER_USER='kyle21'
kubectl create namespace dev --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install course-app `
  homeworks/klymenko-oleksandr/module-04/lesson-12/helm/course-app `
  -n dev `
  --set image.repository="$env:DOCKER_USER/course-app" `
  --set image.tag=1.0.1 `
  --set image.pullPolicy=Always
kubectl logs deploy/course-app-course-app -n dev
kubectl get pods,svc,ingress -n dev

kubectl port-forward svc/course-app-course-app -n dev 8080 
```

## 5. Прибирання
```bash
kubectl delete namespace dev
kubectl delete namespace dragonfly-system
```
