cd ../../../
docker build -t ypodop/course-app:latest . -f homeworks/ypodop/module3-lesson8/Dockerfile
docker push ypodop/course-app:latest
cd homeworks/ypodop/module3-lesson8
docker run --rm -v "./certs:/certs" alpine:3 sh -c "apk add --no-cache openssl >/dev/null && openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /certs/course-app.key -out /certs/course-app.crt -subj '/CN=kubernetes.docker.internal'"
kubectl create secret tls course-app-tls --key ./certs/course-app.key --cert ./certs/course-app.crt -n course-app
kubectl apply -f k8s.yaml
kubectl apply -f course-app-ingress.yaml