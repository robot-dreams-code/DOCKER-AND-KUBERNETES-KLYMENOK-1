cd ../../../
docker build -t ypodop/course-app:latest . -f homeworks/ypodop/module3-lesson6/Dockerfile
docker push ypodop/course-app:latest
cd homeworks/ypodop/module3-lesson6
kubectl apply -f k8s.yaml