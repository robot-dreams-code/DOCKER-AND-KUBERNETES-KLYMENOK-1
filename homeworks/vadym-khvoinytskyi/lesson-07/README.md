
## Adding configmap

~ k apply -f config.yaml
~ k apply -f deployment.yaml


## Making sure variables from configmap are available in pod

~ k exec -it course-app-6ff989f47b-29v6g -- env | egrep "APP_NAME|APP_LOG_LEVEL|APP_TIMEOUT"
APP_TIMEOUT=5s
APP_NAME=Course App
APP_LOG_LEVEL=info

## Updating configmap

~ k get pods
NAME                          READY   STATUS    RESTARTS   AGE
course-app-6ff989f47b-29v6g   1/1     Running   0          6m27s
...

~ vim config.yaml
~ k apply -f config.yaml
configmap/test-config configured
~ k get pods
NAME                          READY   STATUS    RESTARTS   AGE
course-app-6ff989f47b-29v6g   1/1     Running   0          7m29s
...

~ k exec -it course-app-6ff989f47b-29v6g -- env | egrep "APP_NAME|APP_LOG_LEVEL|APP_TIMEOUT"
APP_TIMEOUT=5s
APP_NAME=Course App
APP_LOG_LEVEL=info

#### so variables were not updated inside pod


## Testing with kubectl edit yields the same result

~ k edit configmap test-config
configmap/test-config edited

~ k exec -it course-app-6ff989f47b-29v6g -- env | egrep "APP_NAME|APP_LOG_LEVEL|APP_TIMEOUT"
APP_TIMEOUT=5s
APP_LOG_LEVEL=info
APP_NAME=Course App
~ k describe configmap test-config
Name:         test-config
Namespace:    rd
Labels:       <none>
Annotations:  <none>

Data
====
APP_LOG_LEVEL:
----
error

APP_NAME:
----
Course App

APP_TIMEOUT:
----
5s


BinaryData
====

Events:  <none>

### redeployes pods and subsequently updates config
~ k rollout restart deployment course-app

## Rolling update
  strategy:
   type: RollingUpdate
   rollingUpdate:
     maxSurge: 1
     maxUnavailable: 1

This strategy ensures there is no performance hit since 9 or 10 containers should be available at any given time. Although update process can be slow because it updates only one cantainer at a time and does not proceed to the next one before previous is up and running.
