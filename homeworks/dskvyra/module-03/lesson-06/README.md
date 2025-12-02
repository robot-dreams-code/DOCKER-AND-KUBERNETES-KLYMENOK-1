# Course App Docker & Kubernetes Deployment Write-Up

## Overview
This project demonstrates building a Docker image for the course-app, pushing it to Docker Hub, deploying it to a Kubernetes cluster (Rancher Desktop), and exposing the app via a NodePort service.

---

## Prerequisites
- Docker installed and logged in (`docker login`)
- Kubernetes cluster available (Rancher Desktop)
- `kubectl` configured

---

## Build and Push Docker Image

1. Navigate to the repo root:
cd <path_to_the_repo>

2. Build Docker image using a specific Dockerfile:
`docker build -f homeworks/dskvyra/module-02/lesson-05/Dockerfile -t holymykolay/course-app:latest apps/course-app`

3. Login to Docker registry (if not logged in):
docker login

4. Push the built image to Docker Hub:
`docker push holymykolay/course-app:latest`

---

## Deploy to Kubernetes

1. Change directory to Kubernetes manifests location:
`cd homeworks/dskvyra/module-03/lesson-06/`

2. Create the namespace to isolate resources:
`kubectl apply -f namespace.yaml`

3. Deploy the application:
`kubectl apply -f deployment.yaml`

4. Create a NodePort service for external access:
`kubectl apply -f service.yaml`

---

## Scale and Update Deployment

1. Edit `deployment.yaml` to change replicas count (e.g., to 5):
`replicas: 5`

2. Apply the updated manifest:
`kubectl apply -f deployment.yaml`

3. Watch rollout status to ensure update success:
`kubectl rollout status deployment/course-app -n course-app-ns`

---

## Access the Application

Open your browser and navigate to:
http://localhost:30080
(Replace `30080` with your NodePort if different)

---

## Notes

- The NodePort service exposes the app on each node's IP at the specified port for external access.
- The namespace specified in manifests matches when running `kubectl` commands.
- Labels in manifests ensure correct service-to-pod traffic routing.