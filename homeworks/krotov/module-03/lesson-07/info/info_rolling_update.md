

# For the start: application succesfully deployed with 10 replicas: 

PS C:\Users\usaername> kubectl get deploy -n krotovhh
NAME                                    READY   UP-TO-DATE   AVAILABLE   AGE
python-course-app-deployment            2/2     2            2           3d18h
python-course-app-lesson07-deployment   10/10   10           10          85s

PS C:\Users\usaername> kubectl get pods -n krotovhh
NAME                                                     READY   STATUS    RESTARTS      AGE
python-course-app-deployment-75d6c9d48f-888pq            1/1     Running   5 (10m ago)   3d18h
python-course-app-deployment-75d6c9d48f-xfsjb            1/1     Running   4 (10m ago)   3d3h
python-course-app-lesson07-deployment-5786f56867-84lhd   1/1     Running   0             94s
python-course-app-lesson07-deployment-5786f56867-979cc   1/1     Running   0             94s
python-course-app-lesson07-deployment-5786f56867-cm465   1/1     Running   0             94s
python-course-app-lesson07-deployment-5786f56867-cvf45   1/1     Running   0             94s
python-course-app-lesson07-deployment-5786f56867-gc4vb   1/1     Running   0             94s
python-course-app-lesson07-deployment-5786f56867-h2t7h   1/1     Running   0             94s
python-course-app-lesson07-deployment-5786f56867-j9z8h   1/1     Running   0             94s
python-course-app-lesson07-deployment-5786f56867-mfxz8   1/1     Running   0             94s
python-course-app-lesson07-deployment-5786f56867-w444w   1/1     Running   0             94s
python-course-app-lesson07-deployment-5786f56867-ww9km   1/1     Running   0             94s
redis                                                    1/1     Running   3 (10m ago)   3d18h


# Changing Configmap values of image version from 1.0 tag 2.0 and applying it via kubectl 

PS C:\Users\usaername\Documents\repos\DOCKER-AND-KUBERNETES-KLYMENOK-1\homeworks\krotov\module-03\lesson-07\k8s> kubectl apply -f .\deployment.yml
deployment.apps/python-course-app-lesson07-deployment configured

# Watching rollout start 

PS C:\Users\usaername\Documents\repos\DOCKER-AND-KUBERNETES-KLYMENOK-1\homeworks\krotov\module-03\lesson-07\k8s> kubectl get deploy -n krotovhh
NAME                                    READY   UP-TO-DATE   AVAILABLE   AGE
python-course-app-deployment            2/2     2            2           3d18h
python-course-app-lesson07-deployment   6/10    5            6           12m
PS C:\Users\usaername\Documents\repos\DOCKER-AND-KUBERNETES-KLYMENOK-1\homeworks\krotov\module-03\lesson-07\k8s> kubectl get pods -n krotovhh
NAME                                                     READY   STATUS              RESTARTS      AGE
python-course-app-deployment-75d6c9d48f-888pq            1/1     Running             5 (21m ago)   3d18h
python-course-app-deployment-75d6c9d48f-xfsjb            1/1     Running             4 (21m ago)   3d3h
python-course-app-lesson07-deployment-5786f56867-979cc   1/1     Running             0             13m
python-course-app-lesson07-deployment-5786f56867-cm465   1/1     Running             0             13m
python-course-app-lesson07-deployment-5786f56867-cvf45   1/1     Running             0             13m
python-course-app-lesson07-deployment-5786f56867-h2t7h   1/1     Running             0             13m
python-course-app-lesson07-deployment-5786f56867-mfxz8   1/1     Running             0             13m
python-course-app-lesson07-deployment-5786f56867-ww9km   1/1     Running             0             13m
python-course-app-lesson07-deployment-bc5577cd4-22sjn    0/1     ContainerCreating   0             4s
python-course-app-lesson07-deployment-bc5577cd4-lf2bb    0/1     ContainerCreating   0             4s
python-course-app-lesson07-deployment-bc5577cd4-q5ch2    0/1     ContainerCreating   0             4s
python-course-app-lesson07-deployment-bc5577cd4-xkcnw    0/1     ContainerCreating   0             4s
python-course-app-lesson07-deployment-bc5577cd4-zzvmg    0/1     ContainerCreating   0             4s
redis                                                    1/1     Running             3 (21m ago)   3d18h


PS C:\Users\usaername\Documents\repos\DOCKER-AND-KUBERNETES-KLYMENOK-1\homeworks\krotov\module-03\lesson-07\k8s> kubectl rollout status deploy/python-course-app-lesson07-deployment -n krotovhh
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 5 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 7 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 8 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 8 out of 10 new replicas have been updated...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 3 old replicas are pending termination...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 1 old replicas are pending termination...
Waiting for deployment "python-course-app-lesson07-deployment" rollout to finish: 1 old replicas are pending termination...
deployment "python-course-app-lesson07-deployment" successfully rolled out

# App was rolled out successfully 
