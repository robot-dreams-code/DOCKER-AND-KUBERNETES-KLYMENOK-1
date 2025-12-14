Launch
=====

1) ``kubectl create namespace dragonfly-system``
2) ``kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml``
3) Check pods ``kubectl -n dragonfly-operator-system get pods``  
4) ``kubectl apply -f k8s/dragonfly-cluster.yaml``
5) ``kubectl get dragonflies.dragonflydb.io -A``
6) ```
    kubectl -n dragonfly-operator-system get pods
    kubectl -n dragonfly-operator-system get svc
   ```
7) Enter to pod ``kubectl -n dragonfly-operator-system run redis-client --rm -it --image=redis -- bash``
8) Check status ``redis-cli -h dragonfly-sample -p 6379 ping``