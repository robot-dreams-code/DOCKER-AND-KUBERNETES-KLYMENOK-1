✗ k get endpoints
Warning: v1 Endpoints is deprecated in v1.33+; use discovery.k8s.io/v1 EndpointSlice


✗ k exec -it course-app-6ff989f47b-2jtc9 -- sh
/app # nslookup backend
Server:		10.43.0.10
Address:	10.43.0.10:53

** server can't find backend.cluster.local: NXDOMAIN

** server can't find backend.cluster.local: NXDOMAIN

Name:	backend.rd.svc.cluster.local
Address: 10.43.60.189


** server can't find backend.svc.cluster.local: NXDOMAIN

** server can't find backend.svc.cluster.local: NXDOMAIN


## zero downtime

### deleting pod
find out pods ip addresses with k describe pod
deleting any pod
checking that this ip address was deleted from k describe ingress and/or k describe endpointslice

### tempering with healthz endpoint

add args to container definition in manifest to enable hot reload on uvicorn. Otherwise was not possible to test since killing uvicorn would recreate container and changes to main.py would be gone.
comment out healthz endpoint in main.py
result: ip is gone from ingress, but still listed in endpointslice, pod's status is 0/1

✗ k describ
e ingress
Name:             course-app-ingress
Labels:           <none>
Namespace:        rd
Address:          192.168.69.3
Ingress Class:    traefik
Default backend:  <default>
Rules:
  Host        Path  Backends
  ----        ----  --------
  *
              /   backend:80 (10.42.0.220:8080,10.42.0.221:8080,10.42.0.223:8080 + 7 more...)
Annotations:  <none>
Events:       <none>

 k describ
e pod course-app-65d8cf4758-hz8zh
Name:             course-app-65d8cf4758-hz8zh
Namespace:        rd
Priority:         0
Service Account:  default
Node:             lima-rancher-desktop/192.168.5.15
Start Time:       Sat, 29 Nov 2025 18:51:06 +0100
Labels:           app=course-app
                  pod-template-hash=65d8cf4758
Annotations:      <none>
Status:           Running
IP:               10.42.0.220
IPs:
  IP:           10.42.0.220
Controlled By:  ReplicaSet/course-app-65d8cf4758
Containers:
  course-app:
    Container ID:  docker://633bef2ae283fc6497663402869c10d8288fb2abed5c495b7704916ac1075c0c
    Image:         ghcr.io/vadymkhvoinytskyi/course-app:latest
    Image ID:      docker-pullable://ghcr.io/vadymkhvoinytskyi/course-app@sha256:6aaf33701cc9e458cd5d573fecaa1b5880100614be50730d09a8ec29a8174427
    Port:          8080/TCP
    Host Port:     0/TCP
    Args:
      uvicorn
      src.main:app
      --host
      0.0.0.0
      --port
      8080
      --reload
    State:          Running
      Started:      Sat, 29 Nov 2025 18:51:07 +0100
    Ready:          True
    Restart Count:  0
    Liveness:       tcp-socket :8080 delay=15s timeout=1s period=10s #success=1 #failure=3
    Readiness:      http-get http://:8080/healthz delay=3s timeout=1s period=3s #success=1 #failure=3
    Environment Variables from:
      test-config  ConfigMap  Optional: false
    Environment:   <none>
    Mounts:
      /var/run/secrets/kubernetes.io/serviceaccount from kube-api-access-mstkr (ro)
Conditions:
  Type                        Status
  PodReadyToStartContainers   True
  Initialized                 True
  Ready                       True
  ContainersReady             True
  PodScheduled                True
Volumes:
  kube-api-access-mstkr:
    Type:                    Projected (a volume that contains injected data from multiple sources)
    TokenExpirationSeconds:  3607
    ConfigMapName:           kube-root-ca.crt
    Optional:                false
    DownwardAPI:             true
QoS Class:                   BestEffort
Node-Selectors:              <none>
Tolerations:                 node.kubernetes.io/not-ready:NoExecute op=Exists for 300s
                             node.kubernetes.io/unreachable:NoExecute op=Exists for 300s
Events:
  Type    Reason     Age   From               Message
  ----    ------     ----  ----               -------
  Normal  Scheduled  82s   default-scheduler  Successfully assigned rd/course-app-65d8cf4758-hz8zh to lima-rancher-desktop
  Normal  Pulling    82s   kubelet            Pulling image "ghcr.io/vadymkhvoinytskyi/course-app:latest"
  Normal  Pulled     81s   kubelet            Successfully pulled image "ghcr.io/vadymkhvoinytskyi/course-app:latest" in 1.001s (1.001s including waiting). Image size: 119930991 bytes.
  Normal  Created    81s   kubelet            Created container: course-app
  Normal  Started    81s   kubelet            Started container course-app

k exec -i
t course-app-65d8cf4758-hz8zh -- sh
/app # vi src/main.py # comment out healtz endpoint
/app # exit


## https

openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout tls.key -out tls.crt -subj "/CN=course-app.local"

kubectl create secret tls course-app-tls \
  --cert=tls.crt \
  --key=tls.key
