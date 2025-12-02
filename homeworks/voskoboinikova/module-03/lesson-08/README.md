kubectl delete ns lesson07
kubectl create namespace lesson07
kubectl apply -f . 

# make sure the ports are set correctly for the internal interaction in cluster
kubectl get pods -n lesson07
## - we get here out app start page:
kubectl exec -it <pod-name> -n lesson07 -- wget -qO- http://course-app-svc:80 >output.html
kubectl exec -it course-app-88c59fb4b-b4qx9  -n lesson07 -- wget -qO- http://course-app-svc:80 >output.html

# Zero Downtime Test - failed readiness check:
## get endpoints list:
kubectl get endpoints -n lesson07 -o yaml >output/endpoints.yaml

  kind: Endpoints
  metadata:
    annotations:
      endpoints.kubernetes.io/last-change-trigger-time: "2025-11-28T14:11:44Z"
    creationTimestamp: "2025-11-28T11:13:29Z"
    labels:
      endpoints.kubernetes.io/managed-by: endpoint-controller
    name: course-app-svc
    namespace: lesson07
    resourceVersion: "179197"
    uid: cf1497b1-2623-42f7-8005-35b529f2fb7b
  subsets:
  - addresses:
    - ip: 10.42.0.114
      nodeName: ho-pc02352
      targetRef:
        kind: Pod
        name: course-app-77d658b65b-lkf92
        namespace: lesson07
        uid: 30085a87-d4af-4a33-a59a-2917bb23ab86
    - ip: 10.42.0.115
      nodeName: ho-pc02352
      targetRef:
        kind: Pod
        name: course-app-77d658b65b-qdcpg
        namespace: lesson07
        uid: f3f74c96-cecc-4894-b50f-db9ed76aca48
    - ip: 10.42.0.116
      nodeName: ho-pc02352
      targetRef:
        kind: Pod
        name: course-app-77d658b65b-xvhj9
        namespace: lesson07
        uid: b9dcacdf-3dda-4358-8f13-d573014806d7
    - ip: 10.42.0.117


## select our 'victim' pod (course-app-77d658b65b-xvhj9) and drop app folders inside
kubectl exec -it course-app-77d658b65b-xvhj9 -n lesson07 -- rm -r src
kubectl exec -it course-app-77d658b65b-xvhj9 -n lesson07 -- rm -r data

kubectl logs course-app-77d658b65b-xvhj9 -n lesson07

INFO:     10.42.0.1:40952 - "GET /readyz HTTP/1.1" 200 OK
INFO:     10.42.0.1:40954 - "GET /healthz HTTP/1.1" 200 OK
INFO:     10.42.0.1:40966 - "GET /readyz HTTP/1.1" 503 Service Unavailable
INFO:     10.42.0.1:40972 - "GET /healthz HTTP/1.1" 200 OK
INFO:     10.42.0.1:44450 - "GET /readyz HTTP/1.1" 503 Service Unavailable
INFO:     10.42.0.1:44462 - "GET /healthz HTTP/1.1" 200 OK


##check endpoints again
kubectl get endpoints -n lesson07 -o yaml >output/endpoints_after.yaml

###and our pod and it's adress is in notReadyAddresses:

    notReadyAddresses:
    - ip: 10.42.0.114
      nodeName: ho-pc02352
      targetRef:
        kind: Pod
        name: course-app-77d658b65b-lkf92
        namespace: lesson07
        uid: 30085a87-d4af-4a33-a59a-2917bb23ab86
    - ip: 10.42.0.115
      nodeName: ho-pc02352
      targetRef:
        kind: Pod
        name: course-app-77d658b65b-qdcpg
        namespace: lesson07
        uid: f3f74c96-cecc-4894-b50f-db9ed76aca48
    - ip: 10.42.0.116
      nodeName: ho-pc02352
      targetRef:
        kind: Pod
        name: course-app-77d658b65b-xvhj9
        namespace: lesson07
        uid: b9dcacdf-3dda-4358-8f13-d573014806d7
