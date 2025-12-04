
# To check Replace update version of image tag is set back to 1.0 
# Replacing configuration:

PS C:\Users\username\Documents\repos\DOCKER-AND-KUBERNETES-KLYMENOK-1\homeworks\krotov\module-03\lesson-07\k8s> kubectl replace -f .\deployment.yml
deployment.apps/python-course-app-lesson07-deployment replaced

# Checking the update status:
PS C:\Users\username\Documents\repos\DOCKER-AND-KUBERNETES-KLYMENOK-1\homeworks\krotov\module-03\lesson-07\k8s> kubectl get pods -n krotovhh
NAME                                                     READY   STATUS              RESTARTS      AGE
python-course-app-deployment-75d6c9d48f-888pq            1/1     Running             5 (43m ago)   3d18h
python-course-app-deployment-75d6c9d48f-xfsjb            1/1     Running             4 (43m ago)   3d4h
python-course-app-lesson07-deployment-5786f56867-jsrwg   1/1     Running             0             65s
python-course-app-lesson07-deployment-5786f56867-l8ts7   1/1     Running             0             69s
python-course-app-lesson07-deployment-5786f56867-n62fl   1/1     Running             0             69s
python-course-app-lesson07-deployment-5786f56867-sgzbk   1/1     Running             0             66s
python-course-app-lesson07-deployment-5786f56867-v5nmq   1/1     Running             0             66s
python-course-app-lesson07-deployment-5786f56867-zc7gm   1/1     Running             0             69s
python-course-app-lesson07-deployment-bc5577cd4-5gs69    0/1     ContainerCreating   0             2s
python-course-app-lesson07-deployment-bc5577cd4-b2fwd    0/1     ContainerCreating   0             2s
python-course-app-lesson07-deployment-bc5577cd4-d28wj    0/1     ContainerCreating   0             2s
python-course-app-lesson07-deployment-bc5577cd4-jbpkc    0/1     ContainerCreating   0             2s
python-course-app-lesson07-deployment-bc5577cd4-pnz47    0/1     ContainerCreating   0             2s
redis                                                    1/1     Running             3 (43m ago)   3d18h


