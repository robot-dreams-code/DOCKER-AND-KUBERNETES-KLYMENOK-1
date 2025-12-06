# Simple App 🐳

## Generate a self-signed SSL certificate using OpenSSL and verify it afterwards
```bash
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -sha256 -days 365 -nodes -subj "/C=XX/ST=StateName/L=Kyiv/O=None/OU=None/CN=127.0.0.1.sslip.io"
openssl x509 -in cert.pem  -text -noout | head -n 10
Certificate:
    Data:
        Version: 3 (0x2)
        Serial Number:
            5b:a6:6b:92:8e:58:76:a7:ca:b2:72:24:dd:de:fe:56:ef:65:46:59
        Signature Algorithm: sha256WithRSAEncryption
        Issuer: C=XX, ST=StateName, L=Kyiv, O=None, OU=None, CN=127-0-0-1.sslip.io
        Validity
            Not Before: Nov 26 08:08:28 2025 GMT
            Not After : Nov 26 08:08:28 2026 GMT

```

## Create Secret for Ingress
```bash
kubectl create secret tls app-tls --cert=cert.pem  --key=key.pem

kubectl get secret
NAME           TYPE                DATA   AGE
app-tls        kubernetes.io/tls   2      2m7s
redis-secret   Opaque              1      5d20h
```

## Create CM
```bash
cat cm.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: course-app-config
data:
  APP_MESSAGE: "Hello World"
  APP_STORE: "redis"

```

## Create Secret for Redis
```bash
cat secret.yml
apiVersion: v1
kind: Secret
metadata:
  name: redis-secret
type: Opaque
stringData:
  APP_REDIS_URL: "redis://:password@redis:6379/0"

```

## Deploy All yml files
```bash
kubectl apply -f cm.yml                    
kubectl apply -f secret.yml 
kubectl apply -f deployment_app.yml
kubectl apply -f deployment_redis.yml
kubectl apply -f svc_app.yml          
kubectl apply -f svc_redis.yml
kubectl apply -f ingress.yml    
```

## Changed type
```bash
grep ClusterIP svc_app.yml
  type: ClusterIP
```

## Added Probes
```bash
grep Probe deployment_app.yml -A9
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
            timeoutSeconds: 2
            failureThreshold: 3
            successThreshold: 1
          livenessProbe:
            httpGet:
              path: /readyz
              port: 8080
            initialDelaySeconds: 15
            periodSeconds: 10
            timeoutSeconds: 2
            failureThreshold: 3
            successThreshold: 1
```


## Deleted Deployment Redis
```bash
kubectl delete -f deployment_redis.yml
```


## Liveness/Readiness Probe Failed
```bash

kubectl describe  pod app-6b9799f974-nk2km

Events:
  Type     Reason     Age                 From               Message
  ----     ------     ----                ----               -------
  Normal   Scheduled  21m                 default-scheduler  Successfully assigned default/app-6b9799f974-nk2km to lima-rancher-desktop
  Normal   Pulled     21m                 kubelet            Successfully pulled image "yurievac/lesson-06:latest" in 1.197s (1.197s including waiting). Image size: 120306738 bytes.
  Warning  Unhealthy  75s (x3 over 95s)   kubelet            Liveness probe failed: HTTP probe failed with statuscode: 503
  Normal   Killing    75s                 kubelet            Container app failed liveness probe, will be restarted
  Warning  Unhealthy  74s (x5 over 101s)  kubelet            Readiness probe failed: HTTP probe failed with statuscode: 503
  Normal   Pulled     72s                 kubelet            Successfully pulled image "yurievac/lesson-06:latest" in 1.199s (1.199s including waiting). Image size: 120306738 bytes.
  Normal   Pulled     66s                 kubelet            Successfully pulled image "yurievac/lesson-06:latest" in 1.288s (1.288s including waiting). Image size: 120306738 bytes.
  Normal   Pulled     42s                 kubelet            Successfully pulled image "yurievac/lesson-06:latest" in 1.184s (1.186s including waiting). Image size: 120306738 bytes.
  Normal   Pulling    10s (x5 over 21m)   kubelet            Pulling image "yurievac/lesson-06:latest"
  Normal   Started    8s (x5 over 21m)    kubelet            Started container app
  Normal   Created    8s (x5 over 21m)    kubelet            Created container: app
  Normal   Pulled     8s                  kubelet            Successfully pulled image "yurievac/lesson-06:latest" in 1.16s (1.16s including waiting). Image size: 120306738 bytes.
  Warning  BackOff    4s (x9 over 63s)    kubelet            Back-off restarting failed container app in pod app-6b9799f974-nk2km_default(3a62b60d-763f-4be4-8d7c-18cc7c24a992)
  ```

## Deploy Redis
```bash
kubectl apply -f deployment_redis.yml
deployment.apps/redis created

kubectl get pods
NAME                     READY   STATUS             RESTARTS      AGE
app-6b9799f974-bpgx6     0/1     CrashLoopBackOff   5 (55s ago)   23m
app-6b9799f974-c6fcb     0/1     Running            6 (85s ago)   23m
app-6b9799f974-jml6l     0/1     CrashLoopBackOff   5 (62s ago)   23m
app-6b9799f974-mqrjf     0/1     CrashLoopBackOff   5 (63s ago)   23m
app-6b9799f974-nk2km     0/1     CrashLoopBackOff   5 (55s ago)   23m
app-6b9799f974-pxsxh     0/1     CrashLoopBackOff   5 (66s ago)   23m
app-6b9799f974-t7pbb     0/1     CrashLoopBackOff   5 (55s ago)   23m
app-6b9799f974-tsd2b     0/1     CrashLoopBackOff   5 (56s ago)   23m
app-6b9799f974-xcdbx     0/1     CrashLoopBackOff   5 (75s ago)   23m
app-6b9799f974-zzjkr     0/1     CrashLoopBackOff   5 (61s ago)   23m
redis-86b8bf8458-9726l   1/1     Running            0             3s
```

## Pods running after Redis startup
```bash
kubectl get pods
NAME                     READY   STATUS    RESTARTS        AGE
app-6b9799f974-bpgx6     1/1     Running   6 (2m20s ago)   24m
app-6b9799f974-c6fcb     1/1     Running   6 (2m50s ago)   24m
app-6b9799f974-jml6l     1/1     Running   6 (2m27s ago)   24m
app-6b9799f974-mqrjf     1/1     Running   6 (2m28s ago)   24m
app-6b9799f974-nk2km     1/1     Running   6 (2m20s ago)   24m
app-6b9799f974-pxsxh     1/1     Running   6 (2m31s ago)   24m
app-6b9799f974-t7pbb     1/1     Running   6 (2m20s ago)   24m
app-6b9799f974-tsd2b     1/1     Running   6 (2m21s ago)   24m
app-6b9799f974-xcdbx     1/1     Running   6 (2m40s ago)   24m
app-6b9799f974-zzjkr     1/1     Running   6 (2m26s ago)   24m
redis-86b8bf8458-9726l   1/1     Running   0               88s
```

## Check App
```bash
curl https://127-0-0-1.sslip.io/ -kv
* Host 127-0-0-1.sslip.io:443 was resolved.
* IPv6: (none)
* IPv4: 127.0.0.1
*   Trying 127.0.0.1:443...
* Connected to 127-0-0-1.sslip.io (127.0.0.1) port 443
* ALPN: curl offers h2,http/1.1
* (304) (OUT), TLS handshake, Client hello (1):
* (304) (IN), TLS handshake, Server hello (2):
* (304) (IN), TLS handshake, Unknown (8):
* (304) (IN), TLS handshake, Certificate (11):
* (304) (IN), TLS handshake, CERT verify (15):
* (304) (IN), TLS handshake, Finished (20):
* (304) (OUT), TLS handshake, Finished (20):
* SSL connection using TLSv1.3 / AEAD-CHACHA20-POLY1305-SHA256 / [blank] / UNDEF
* ALPN: server accepted h2
* Server certificate:
*  subject: C=XX; ST=StateName; L=Kyiv; O=None; OU=None; CN=127-0-0-1.sslip.io
*  start date: Nov 26 08:08:28 2025 GMT
*  expire date: Nov 26 08:08:28 2026 GMT
*  issuer: C=XX; ST=StateName; L=Kyiv; O=None; OU=None; CN=127-0-0-1.sslip.io
*  SSL certificate verify result: self signed certificate (18), continuing anyway.
* using HTTP/2
* [HTTP/2] [1] OPENED stream for https://127-0-0-1.sslip.io/
* [HTTP/2] [1] [:method: GET]
* [HTTP/2] [1] [:scheme: https]
* [HTTP/2] [1] [:authority: 127-0-0-1.sslip.io]
* [HTTP/2] [1] [:path: /]
* [HTTP/2] [1] [user-agent: curl/8.7.1]
* [HTTP/2] [1] [accept: */*]
> GET / HTTP/2
> Host: 127-0-0-1.sslip.io
> User-Agent: curl/8.7.1
> Accept: */*
>
* Request completely sent off
< HTTP/2 200
< content-type: text/html; charset=utf-8
< date: Wed, 26 Nov 2025 08:31:16 GMT
< server: uvicorn
< x-request-id: 5cc82cbf43a9
< content-length: 11943

```
