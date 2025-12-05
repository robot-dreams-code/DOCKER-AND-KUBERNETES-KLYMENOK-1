kubectl delete -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
curl -LO https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
kubectl apply -k .
kubectl apply -f dragonfly-cluster.yaml