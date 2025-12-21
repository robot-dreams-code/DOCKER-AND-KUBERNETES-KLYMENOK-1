# create initial structure for course-app, edit files and deploy
helm create course-app
helm install course-app-inst course-app --namespace lesson11 --create-namespace

#add bitnami repositary and install redis 
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo update
##somehow installed redis, with latest version I have 403 error, so I use bitnami/redis version 20 
## and specify corp harbor in image.registry and also use old bitnami repository (for older versions of redis)
##(chat gpt says that Redis charts AFTER ~20.x are published ONLY as OCI artifacts on Docker Hub -> blocked in corporate networks, I did not managed to find setttings to overcome that )
helm install redis bitnami/redis --set auth.password="pwd"  --namespace lesson11  --version 20.0.0 --set image.registry=corp/proxy --set image.repository=bitnamilegacy/redis

#update course-app setting and update chart
helm upgrade course-app-inst course-app --version 0.1.1  --namespace lesson11
kubectl rollout restart deployment course-app-inst -n lesson11


##helm list -n lesson11 
NAME           	NAMESPACE	REVISION	UPDATED                              	STATUS  	CHART           	APP VERSION
course-app-inst	lesson11 	2       	2025-12-05 22:12:30.1788451 +0200 EET	deployed	course-app-0.1.1	1.0 
redis          	lesson11 	1       	2025-12-05 21:37:05.211033 +0200 EET 	deployed	redis-20.0.0    	7.4. 


##kubectl get all -n lesson11
NAME                                   READY   STATUS    RESTARTS   AGE
pod/course-app-inst-5b9b7648c5-26rc5   1/1     Running   0          10m
pod/course-app-inst-5b9b7648c5-42jdz   1/1     Running   0          10m
pod/course-app-inst-5b9b7648c5-fzglv   1/1     Running   0          10m
pod/course-app-inst-5b9b7648c5-gkvf7   1/1     Running   0          10m
pod/course-app-inst-5b9b7648c5-h58zt   1/1     Running   0          10m
pod/course-app-inst-5b9b7648c5-pslrr   1/1     Running   0          10m
pod/course-app-inst-5b9b7648c5-sbjqk   1/1     Running   0          10m
pod/course-app-inst-5b9b7648c5-scth4   1/1     Running   0          10m
pod/course-app-inst-5b9b7648c5-t2lh5   1/1     Running   0          10m
pod/course-app-inst-5b9b7648c5-tf9bx   1/1     Running   0          10m
pod/course-app-inst-5b9b7648c5-z8tds   1/1     Running   0          10m
pod/redis-master-0                     1/1     Running   0          37m
pod/redis-replicas-0                   1/1     Running   0          37m
pod/redis-replicas-1                   1/1     Running   0          36m
pod/redis-replicas-2                   1/1     Running   0          36m

NAME                      TYPE        CLUSTER-IP     EXTERNAL-IP   PORT(S)    AGE
service/course-app-inst   ClusterIP   10.43.11.154   <none>        80/TCP     10m
service/redis-headless    ClusterIP   None           <none>        6379/TCP   37m
service/redis-master      ClusterIP   10.43.144.66   <none>        6379/TCP   37m
service/redis-replicas    ClusterIP   10.43.254.54   <none>        6379/TCP   37m

NAME                              READY   UP-TO-DATE   AVAILABLE   AGE
deployment.apps/course-app-inst   11/11   11           11          10m

NAME                                         DESIRED   CURRENT   READY   AGE
replicaset.apps/course-app-inst-5b9b7648c5   11        11        11      10m

NAME                              READY   AGE
statefulset.apps/redis-master     1/1     37m
statefulset.apps/redis-replicas   3/3     37m


## check how our templates are filled fron values
helm template course-app-inst course-app 

---
# Source: course-app/templates/app-config-map.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: course-app-inst-config-map
data:
  APP_MESSAGE: Hello And Welcome To Course App! Nice to see you here!
  APP_STORE: redis
  APP_REDIS_URL: redis://:pwd@redis-master:6379/0
---
# Source: course-app/templates/app-service.yaml
apiVersion: v1
kind: Service
metadata:
  name: course-app-inst
spec:
  type: ClusterIP
  selector:
    app.kubernetes.io/name: course-app
    app.kubernetes.io/instance: course-app-inst
  ports:
    - port: 80
      targetPort: 8080
      protocol: TCP
      name: http
---
# Source: course-app/templates/app-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: course-app-inst
spec:
  replicas: 11
  selector:
    matchLabels:
      app.kubernetes.io/name: course-app
      app.kubernetes.io/instance: course-app-inst
  template:
    metadata:
      labels:
        helm.sh/chart: course-app-0.1.1
        app.kubernetes.io/name: course-app
        app.kubernetes.io/instance: course-app-inst
        app.kubernetes.io/version: "1.0"
        app.kubernetes.io/managed-by: Helm
    spec:
      imagePullSecrets:
        - name: harbor-secret
      containers:
        - name: course-app
          image: "demo.goharbor.io/lesson06/course-app:v1.0"
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
                name: course-app-inst-config-map
---
# Source: course-app/templates/app-ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: course-app-inst
spec:
  ingressClassName: traefik
  rules:
    - host: "course-app.local"
      http:
        paths:
          - path: /
            pathType: ImplementationSpecific
            backend:
              service:
                name: course-app-inst
                port:
                  number: 80
