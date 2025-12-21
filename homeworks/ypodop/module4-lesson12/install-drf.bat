kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
kubectl get pods -n dragonfly-operator-system
kubectl get deployments -n dragonfly-operator-system