curl -LO https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
kubectl apply -k .
kubectl apply -f dragonfly.yaml

#restarting helm from previous lesson with dragonfly  
helm upgrade --install course-app-inst ../lesson11/course-app   -n lesson11   -f values.yaml --set replicaCount=0
helm upgrade --install course-app-inst ../lesson11/course-app   -n lesson11   -f values.yaml --set replicaCount=12

kubectl apply -f rbac.yaml

#output of can-i is in screenshot

