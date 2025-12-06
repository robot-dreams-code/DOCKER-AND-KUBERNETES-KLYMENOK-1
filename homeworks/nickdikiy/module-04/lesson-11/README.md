# 1. Ініціалізуємо чарт
```bash
helm create course-app
```

# 2. Namespace можна задавати через values.yaml, або при install/upgrade. Останній варіант більш поширений
```bash 
helm install myapp ./myapp --namespace my-namespace
```

# 3. Опишемо values для deployment:
```
replicaCount: 3
image:
  repository: nickdikiynd/course-app
  pullPolicy: IfNotPresent
  tag: "1.0"
```

# 4. Опишемо values для service:
```
service:
  type: ClusterIP
  port: 80
  targetPort: 8080
```


# 5. Опишемо values для ingress:
```
ingress:
  enabled: true
  className: "traefik"
  annotations: {}
  hosts:
    - host: course-app.local
      paths:
        - path: /
          pathType: Prefix
  tls: []
```


# 6. Для redis додамо репозиторій bitnami:
```bash
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
helm search repo bitnami/redis
```
```
NAME                    CHART VERSION   APP VERSION     DESCRIPTION                                       
bitnami/redis           24.0.0          8.4.0           Redis(R) is an open source, advanced key-value ...
bitnami/redis-cluster   13.0.4          8.2.1           Redis(R) is an open source, scalable, distribut...
```

# 7. Створимо values для redis і переглянемо його вміст:
```bash
helm template redis bitnami/redis -f ./course-app/bitnami-redis-values.yaml
```


# 8. Прокидуватимемо змінні оточення через configMap, для цього створимо шаблон configmap.yaml:
```
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ .Values.envConfigMap.name }}
data:
{{- range $key, $value := .Values.envConfigMap.data }}
  {{ $key }}: {{ $value | quote }}
{{- end }}
```


# 9. Додамо змінні оточення в values.yaml:
```
envConfigMap:
    name: course-app-config
    data:
        APP_STORE: "redis-master"
        APP_REDIS_URL: "redis://redis-master:6379"
```


# 11. Оновимо deployment.yaml:
```
{{- with .Values.envConfigMap }}
envFrom:
- configMapRef: 
    name: {{ .name }}
{{- end }}
```


# 12. Перевіримо шаблони для цих ресурсів:
```bash
helm template course-app ./course-app -s templates/deployment.yaml
```
```
# Source: course-app/templates/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: course-app
  labels:
    helm.sh/chart: course-app-1.0.0
    app.kubernetes.io/name: course-app
    app.kubernetes.io/instance: course-app
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  replicas: 5
  selector:
    matchLabels:
      app.kubernetes.io/name: course-app
      app.kubernetes.io/instance: course-app
  template:
    metadata:
      labels:
        helm.sh/chart: course-app-1.0.0
        app.kubernetes.io/name: course-app
        app.kubernetes.io/instance: course-app
        app.kubernetes.io/version: "1.0.0"
        app.kubernetes.io/managed-by: Helm
    spec:
      serviceAccountName: course-app
      containers:
        - name: course-app
          image: "nickdikiynd/course-app:1.0"
          imagePullPolicy: IfNotPresent
          ports:
            - name: http
              containerPort: 80
              protocol: TCP
          livenessProbe:
            httpGet:
              path: /healthz
              port: 8080
          readinessProbe:
            httpGet:
              path: /readyz
              port: 8080
          envFrom:
            - configMapRef:
                name: course-app-config
```

```bash
helm template course-app ./course-app -s templates/service.yaml
```
```
# Source: course-app/templates/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: course-app
  labels:
    helm.sh/chart: course-app-1.0.0
    app.kubernetes.io/name: course-app
    app.kubernetes.io/instance: course-app
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  type: ClusterIP
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
      name: http
  selector:
    app.kubernetes.io/name: course-app
    app.kubernetes.io/instance: course-app        
```

```bash
helm template course-app ./course-app -s templates/ingress.yaml
```
```
# Source: course-app/templates/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: course-app
  labels:
    helm.sh/chart: course-app-1.0.0
    app.kubernetes.io/name: course-app
    app.kubernetes.io/instance: course-app
    app.kubernetes.io/version: "1.0.0"
    app.kubernetes.io/managed-by: Helm
spec:
  ingressClassName: traefik
  rules:
    - host: "course-app.local"
      http:
        paths:
          - path: /
            pathType: Prefix
            backend:
              service:
                name: course-app
                port:
                  number: 80
```


# 12. Проведемо деплой застосунку:
* Спершу redis:
``` bash
helm install redis bitnami/redis -f ./course-app/bitnami-redis-values.yaml
```
* Далі сам додаток:
``` bash
helm install course-app ./course-app
```

```
helm list                           
NAME            NAMESPACE       REVISION        UPDATED                                 STATUS          CHART                   APP VERSION
course-app      default         1               2025-12-06 16:22:01.953937 +0200 EET    deployed        course-app-1.0.0        1.0.0      
redis           default         1               2025-12-06 16:21:59.936562 +0200 EET    deployed        redis-24.0.0            8.4.0    

kubectl get pvc    
NAME                          STATUS   VOLUME                                     CAPACITY   ACCESS MODES   STORAGECLASS   VOLUMEATTRIBUTESCLASS   AGE
redis-data-redis-master-0     Bound    pvc-42351537-0d02-4fe9-a3a7-cbbc62982eb0   8Gi        RWO            local-path     <unset>                 37m
redis-data-redis-replicas-0   Bound    pvc-ccef8541-2dbe-49e9-b58a-beefe775ff85   8Gi        RWO            local-path     <unset>                 37m
redis-data-redis-replicas-1   Bound    pvc-50b8d7e7-3079-4e69-9ce1-036903445585   8Gi        RWO            local-path     <unset>                 37m

kubectl get pods
NAME                          READY   STATUS    RESTARTS   AGE
course-app-7c55cf5d6f-4scwk   1/1     Running   0          54s
course-app-7c55cf5d6f-m25vb   1/1     Running   0          54s
course-app-7c55cf5d6f-mnxhq   1/1     Running   0          54s
course-app-7c55cf5d6f-pvhzh   1/1     Running   0          54s
course-app-7c55cf5d6f-wt25r   1/1     Running   0          54s
redis-master-0                1/1     Running   0          56s
redis-replicas-0              1/1     Running   0          56s
redis-replicas-1              1/1     Running   0          25s

kubectl get svc
NAME             TYPE        CLUSTER-IP      EXTERNAL-IP   PORT(S)    AGE
course-app       ClusterIP   10.43.167.253   <none>        80/TCP     66s
kubernetes       ClusterIP   10.43.0.1       <none>        443/TCP    39m
redis-headless   ClusterIP   None            <none>        6379/TCP   68s
redis-master     ClusterIP   10.43.123.12    <none>        6379/TCP   68s
redis-replicas   ClusterIP   10.43.129.20    <none>        6379/TCP   68s

kubectl get endpoints
NAME             ENDPOINTS                                                        AGE
course-app       10.42.0.198:8080,10.42.0.199:8080,10.42.0.200:8080 + 2 more...   77s
kubernetes       192.168.64.2:6443                                                39m
redis-headless   10.42.0.196:6379,10.42.0.197:6379,10.42.0.203:6379               79s
redis-master     10.42.0.196:6379                                                 79s
redis-replicas   10.42.0.197:6379,10.42.0.203:6379                                79s
```


# 13. Перевіримо що додаток працює:
```
curl -o /dev/null -s -w "%{http_code}\n" http://course-app.local/
200
```