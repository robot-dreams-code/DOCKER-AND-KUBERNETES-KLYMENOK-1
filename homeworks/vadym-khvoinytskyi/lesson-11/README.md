#

## to copy secret to another namespace

kubectl get secrets github -n rd -o json \
 | jq 'del(.metadata["namespace","creationTimestamp","resourceVersion","selfLink","uid","annotations"])' \
 | kubectl apply -n test-helm -f -

## install helm chart

helm install helm-course ./course-app

# Bitname redis

helm install my-redis bitnami/redis
helm install my-app ./course-app-without-redis --set redisName=my-redis-master
k log my-app-course-app-896d87b45-kh54c  # showed that redis required auth, but app doesn't support it'
helm upgrade my-redis bitnami/redis --set auth.enabled=false
