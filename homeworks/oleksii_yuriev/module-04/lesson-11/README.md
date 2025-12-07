# Simple App 🐳

## Create NS
```bash
kubectl create ns dev
```

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

## Create CM
```bash
cat cm.yml
apiVersion: v1
kind: ConfigMap
metadata:
  name: course-app-config
  namespace: dev
data:
  APP_MESSAGE: Hello World!!!
  APP_STORE: redis
  LANG: en_US.UTF-8
  LANGUAGE: en_US:en
  LC_ALL: en_US.UTF-8
  TZ: Europe/Kiev

```

## Create Secret with Redis Connection String
```bash
cat secret.yml
apiVersion: v1
kind: Secret
metadata:
  name: redis-secret
  namespace: dev
type: Opaque
stringData:
  APP_REDIS_URL: "redis://:password@redis-master:6379/0"


## Apply CM and Secret
```bash
kubectl apply -f secret.yml
kubectl apply -f cm.yml

```

## Install Redis using the Bitnami Helm Chart
```bash
helm install redis --set auth.password=password oci://registry-1.docker.io/bitnamicharts/redis --namespace dev
```

## Create a New Helm Chart
```bash
helm create app
```

## Update Deployment Template
```bash
vi templates/deployment.yaml

.....
          {{- if .Values.envFrom }}
          envFrom:
{{ toYaml .Values.envFrom | indent 12 }}
          {{- end }}
          {{- if .Values.env }}
          env:
{{ toYaml .Values.env | indent 12 }}
          {{- end }}
```

## Update values.yaml
```bash
vi values.yaml

.....
image:
  repository: yurievac/lesson-06
  # This sets the pull policy for images.
  pullPolicy: IfNotPresent
  # Overrides the image tag whose default is the chart appVersion.
  tag: "latest"


envFrom:
  - configMapRef:
      name: course-app-config

env:
  - name: APP_REDIS_URL
    valueFrom:
      secretKeyRef:
        name: redis-secret
        key: APP_REDIS_URL

......

ingress:
  enabled: true
  className: ""
  annotations: {}
    # kubernetes.io/ingress.class: nginx
    # kubernetes.io/tls-acme: "true"
  hosts:
    - host: 127-0-0-1.sslip.io
      paths:
        - path: /
          pathType: ImplementationSpecific
  tls:
    - secretName: app-tls
      hosts:
        - 127-0-0-1.sslip.io

......

livenessProbe:
  httpGet:
    path: /readyz
    port: http
readinessProbe:
  httpGet:
    path: /readyz
    port: http

```

## Deploy the Application via Helm
```bash
helm install app . -f values.yaml
NAME: app
LAST DEPLOYED: Sun Dec  7 12:37:26 2025
NAMESPACE: dev
STATUS: deployed
REVISION: 1
NOTES:
1. Get the application URL by running these commands:
  https://127-0-0-1.sslip.io/

```