## Install Dragonfly CRD and Operator 
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml

namespace/dragonfly-operator-system created
customresourcedefinition.apiextensions.k8s.io/dragonflies.dragonflydb.io created
serviceaccount/dragonfly-operator-controller-manager created
role.rbac.authorization.k8s.io/dragonfly-operator-leader-election-role created
clusterrole.rbac.authorization.k8s.io/dragonfly-operator-manager-role created
clusterrole.rbac.authorization.k8s.io/dragonfly-operator-metrics-reader created
clusterrole.rbac.authorization.k8s.io/dragonfly-operator-proxy-role created
rolebinding.rbac.authorization.k8s.io/dragonfly-operator-leader-election-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/dragonfly-operator-manager-rolebinding created
clusterrolebinding.rbac.authorization.k8s.io/dragonfly-operator-proxy-rolebinding created
service/dragonfly-operator-controller-manager-metrics-service created
deployment.apps/dragonfly-operator-controller-manager created

###but got some problems:
dragonfly-operator-system   dragonfly-operator-controller-manager-97cdfcc85-mrmrn   0/2     ImagePullBackOff   0                8m41s

###and after 
kubectl describe pod dragonfly-operator-controller-manager-97cdfcc85-mrmrn -n dragonfly-operator-system
  Warning  Failed     8m53s  kubelet            Failed to pull image "quay.io/brancz/kube-rbac-proxy:v0.16.0": Error response from daemon: pull access denied for quay.io/brancz/kube-rbac-proxy

###edited deployment images name to include corporate proxies
kubectl edit deployment dragonfly-operator-controller-manager -n dragonfly-operator-system

### and restrted deployment
kubectl rollout restart deployment dragonfly-operator-controller-manager -n dragonfly-operator-system

### checked pods
NAMESPACE                   NAME                                                     READY   STATUS      RESTARTS         AGE
dragonfly-operator-system   dragonfly-operator-controller-manager-67f4886f89-q6cqj   2/2     Running     0                76s


##Create Dragonfly cluster with the help of Dragonfly's CR
### find apiVersion/kind for CR
kubectl get crd | findstr /i "dragonfly"
NAME                                        CREATED AT
dragonflies.dragonflydb.io                  2025-12-04T20:09:11Z

kubectl api-resources | findstr /i dragonfly
NAME                                SHORTNAMES   APIVERSION                          NAMESPACED   KIND
dragonflies                                      dragonflydb.io/v1alpha1             true         Dragonfly

### create and apply Dragonfly instance with replicas
kubectl apply -f dragonfly-cluster.yaml   -> lesson12                    my-dragonfly-0                                           0/1     ImagePullBackOff   0                77s
kubectl describe pod my-dragonfly-0 -n lesson12 ->  Failed to pull image "docker.dragonflydb.io/dragonflydb/dragonfly:v1.35.0": Error response from daemon: pull access denied for docker.dragonflydb.io/dragonflydb/dragonfly

kubectl set image pod my-dragonfly-0 dragonfly=corp-proxy-here/dragonflydb/dragonfly:v1.35.0 -n lesson12

###kubectl get pods -n  lesson12
NAME             READY   STATUS    RESTARTS   AGE
my-dragonfly-0   1/1     Running   0          5m39s
my-dragonfly-1   1/1     Running   0          4m20s
my-dragonfly-2   1/1     Running   0          45s
