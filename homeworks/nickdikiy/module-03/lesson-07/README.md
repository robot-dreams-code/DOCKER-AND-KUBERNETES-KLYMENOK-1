#### Виконуватимемо завдання на основі попереднього.

## 1. Запустимо k8s кластер, очистимо всі дані і проведемо деплой:
```bash
orb start k8s
kubectl delete -k ./
kubectl apply -k ./
```


## 2. Переглянемо events:
```bash
kubectl events -n homework
```
```
LAST SEEN   TYPE     REASON              OBJECT                                        MESSAGE
3s          Normal   Pulled              Pod/course-app-deployment-76d7779784-ggtkh    Container image "nickdikiynd/course-app:1.0" already present on machine
3s          Normal   Created             Pod/course-app-deployment-76d7779784-ggtkh    Created container: course-app
3s          Normal   Started             Pod/course-app-deployment-76d7779784-ggtkh    Started container course-app
3s          Normal   Pulled              Pod/course-app-deployment-76d7779784-kh7ng    Container image "nickdikiynd/course-app:1.0" already present on machine
3s          Normal   Created             Pod/course-app-deployment-76d7779784-kh7ng    Created container: course-app
3s          Normal   Started             Pod/course-app-deployment-76d7779784-kh7ng    Started container course-app
3s          Normal   SuccessfulCreate    ReplicaSet/course-app-deployment-76d7779784   Created pod: course-app-deployment-76d7779784-kh7ng
3s          Normal   SuccessfulCreate    ReplicaSet/course-app-deployment-76d7779784   Created pod: course-app-deployment-76d7779784-ggtkh
3s          Normal   ScalingReplicaSet   Deployment/course-app-deployment              Scaled up replica set course-app-deployment-76d7779784 from 0 to 2
2s          Normal   Scheduled           Pod/course-app-deployment-76d7779784-ggtkh    Successfully assigned homework/course-app-deployment-76d7779784-ggtkh to orbstack
2s          Normal   Scheduled           Pod/course-app-deployment-76d7779784-kh7ng    Successfully assigned homework/course-app-deployment-76d7779784-kh7ng to orbstack
```
#### Можна побачити процес розгортання: 
* Image вже існує локально, тому він не завантажується знову
* Контейнер успішно створений і запущений (REASON: Created, Started)
* ReplicaSet успішно створив Pod-и: (REASON: SuccessfulCreate, SuccessfulCreate)
* Deployment масштабував ReplicaSet з 0 до 2: (REASON: ScalingReplicaSet)
* Scheduler обрав на якій ноді розмістити Pod-и (REASON: Scheduled)
#### Очистити івенти можна командою:
```bash
 kubectl delete events --all -n homework
```


## 3. Додамо initContainers секцію в deployment.yaml:
#### Додамо очікування в 5 секунд перед стартом (імітація виконання залежностей).
```bash
kubectl apply -f deployment.yaml
kubectl apply -f service.yaml
```
#### Ми можемо відслідковувати статус виконанням команди: ```bash  kubectl get pods -n homework```
```
NAME                                     READY   STATUS     RESTARTS   AGE
course-app-deployment-55b6f4ffcd-kds8t   0/1     Init:0/1   0          3s
course-app-deployment-55b6f4ffcd-wvsmh   0/1     Init:0/1   0          3s

NAME                                     READY   STATUS            RESTARTS   AGE
course-app-deployment-55b6f4ffcd-kds8t   0/1     PodInitializing   0          7s
course-app-deployment-55b6f4ffcd-wvsmh   0/1     PodInitializing   0          7s

NAME                                     READY   STATUS    RESTARTS   AGE
course-app-deployment-55b6f4ffcd-kds8t   1/1     Running   0          9s
course-app-deployment-55b6f4ffcd-wvsmh   1/1     Running   0          9s
```
#### Тут ми бачемо, що поди створені, але запускаються вони тільки після того як initContainer завершить свою роботу.
#### Також можемо перевірити логи: ```bash  kubectl logs course-app-deployment-55b6f4ffcd-wvsmh -c init-course-app -n homework```
```
InitContainer starting...
InitContainer finished!
```


## 3. Додамо resource Job - одноразове виконання:
```bash
kubectl apply -f kubernetes-spec-downloader-job.yaml
kubectl get pods -n homework --selector=job-name=kubernetes-spec-downloader-job
kubectl logs kubernetes-spec-downloader-job-6kmjw -c kubernetes-spec-downloader-job -n homework 
```
```
NAME                                   READY   STATUS      RESTARTS   AGE
kubernetes-spec-downloader-job-6kmjw   0/1     Completed   0          57s

Downloading Kubernetes OpenAPI spec...
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100 3756k  100 3756k    0     0  5076k      0 --:--:-- --:--:-- --:--:-- 5083k
Download finished!
```



## 4. Для тестуванні resources створимо stress-job.yaml:
#### Для початку виконаємо команду "stress --vm 1 --vm-bytes 20M --timeout 30s", тобто в межах ліміту
```bash
kubectl apply -f stress-job.yaml
kubectl get pods -n homework --selector=job-name=stress-job
kubectl logs stress-job-p7w7p -c stress-job -n homework 
kubectl events -n homework
```
```
stress: info: [1] dispatching hogs: 0 cpu, 0 io, 1 vm, 0 hdd
stress: info: [1] successful run completed in 30s

2m9s        Normal   Created             Pod/stress-job-p7w7p                          Created container: stress-job
2m9s        Normal   Started             Pod/stress-job-p7w7p                          Started container stress-job
96s         Normal   Completed           Job/stress-job                                Job completed
```
#### Командою kubectl describe pod stress-job-p7w7p -n homework можна перевірити що ліміти були встановлені.
#### Збільшимо кількість споживання памяті "stress --vm 1 --vm-bytes 124M --timeout 30s", тобто в межах ліміту
```bash
kubectl delete job stress-job -n homework
kubectl apply -f stress-job.yaml
kubectl get pods -n homework
```
```
NAME                                     READY   STATUS      RESTARTS   AGE
course-app-deployment-55b6f4ffcd-kds8t   1/1     Running     0          42m
course-app-deployment-55b6f4ffcd-wvsmh   1/1     Running     0          42m
kubernetes-spec-downloader-job-6kmjw     0/1     Completed   0          29m
stress-job-cwhls                         0/1     OOMKilled   0          4s
```



## 5. Створимо ConfigMap, запустимо deployment:
```bash
kubectl apply -f config-map.yaml 
kubectl apply -f deployment.yaml 
kubectl get pods -n homework  
```
```
configmap/course-app-configmap created
deployment.apps/course-app-deployment configured

NAME                                     READY   STATUS     RESTARTS   AGE
course-app-deployment-57748bbd95-s6dkl   0/1     Init:0/1   0          3s
```
#### З часом контейнери запустяться (в нас затримка в 5 секунд в initContainer)
#### Змінимо значення в config map, відстежемо деплой 
```bash
kubectl apply -f config-map.yaml
kubectl get pods -n homework  
```

```
configmap/course-app-configmap configured
NAME                                     READY   STATUS    RESTARTS   AGE
course-app-deployment-57748bbd95-s6dkl   1/1     Running   0          2m17s
```
#### Бачимо що контейнери не перестворються. Для прокидання нових значень використовуємо - ```bash kubectl rollout restart deployment -n homework```
```
deployment.apps/course-app-deployment restarted
NAME                                     READY   STATUS     RESTARTS   AGE
course-app-deployment-57748bbd95-s6dkl   1/1     Running    0          4m11s
course-app-deployment-64bc86bdfd-77vsg   0/1     Init:0/1   0          3s
```

#### Додамо envVar змінну прям в deployment, запустимо деплой, змінимо змінну і знову запустимо деплой
```bash
kubectl apply -f deployment.yaml
kubectl get pods -n homework
```
```
deployment.apps/course-app-deployment configured
NAME                                    READY   STATUS    RESTARTS   AGE
course-app-deployment-d4f4df647-spz86   1/1     Running   0          77s

nickdikiy@MacBook-Pro-Nick lesson-07 % kubectl get pods -n homework    
NAME                                    READY   STATUS     RESTARTS   AGE
course-app-deployment-64fb799b9-kq64r   0/1     Init:0/1   0          1s
course-app-deployment-d4f4df647-spz86   1/1     Running    0          100s
```
#### Бачимо що контейнер перестворюється відразу. Це логічно адже ми змінили сам deployment.

#### Додамо ще один configmap, і підключимо його як файл.
#### Я не хочу змінювати deployment, тому виконаю деплоймент в одноразовому поді:
```bash
kubectl run test-script -n homework --image=nickdikiynd/course-app:1.0 \
  --overrides='
  {
    "spec": {
      "containers": [
        {
          "name": "test",
          "image": "nickdikiynd/course-app:1.0",
          "command": ["sh","-c","sh /scripts/start.sh && sleep 3600"],
          "volumeMounts":[{"name":"script-volume","mountPath":"/scripts","readOnly":true}]
        }
      ],
      "volumes":[{"name":"script-volume","configMap":{"name":"file-course-app-configmap"}}]
    }
  }'
```
```
kubectl get  pods -n homework                                                                                                       
NAME                                    READY   STATUS    RESTARTS   AGE
course-app-deployment-c778f8d7b-v55bf   1/1     Running   0          106s
test-script                             1/1     Running   0          11s

kubectl logs test-script -n homework                                                                                                      
Hello from ConfigMap script!
This is running inside the container.
```
#### Бачимо що контейнер запустився, і виконав скрипт змонтований в волюм.



## 6. Збільшимо кількість реплік до 10, зменшимо затримку до 1 секунди (initContainers):
```bash
kubectl apply -f  deployment.yaml
kubectl get pods -n homework
```
```
NAME                                     READY   STATUS    RESTARTS   AGE
course-app-deployment-55fb748b47-2w249   1/1     Running   0          5s
course-app-deployment-55fb748b47-4jxdt   1/1     Running   0          6s
course-app-deployment-55fb748b47-ct6lt   1/1     Running   0          9s
course-app-deployment-55fb748b47-cwhll   1/1     Running   0          9s
course-app-deployment-55fb748b47-dgtvv   1/1     Running   0          9s
course-app-deployment-55fb748b47-fjfvp   1/1     Running   0          6s
course-app-deployment-55fb748b47-hswft   1/1     Running   0          9s
course-app-deployment-55fb748b47-mwdg7   1/1     Running   0          6s
course-app-deployment-55fb748b47-pwsvb   1/1     Running   0          9s
course-app-deployment-55fb748b47-s2pht   1/1     Running   0          6s
```
####  Додамо Recreate стратегію перезапустимо деплой.
```bash
kubectl apply -f  deployment.yaml
kubectl rollout restart deployment -n homework
```
```
NAME                                     READY   STATUS     RESTARTS   AGE
course-app-deployment-6b8cffdd64-bzkk9   0/1     Init:0/1   0          0s
course-app-deployment-6b8cffdd64-k8f7p   0/1     Init:0/1   0          0s
course-app-deployment-6b8cffdd64-kwzg4   0/1     Init:0/1   0          0s
course-app-deployment-6b8cffdd64-lfqzp   0/1     Init:0/1   0          0s
course-app-deployment-6b8cffdd64-n9gd5   0/1     Init:0/1   0          0s
course-app-deployment-6b8cffdd64-pdrht   0/1     Init:0/1   0          0s
course-app-deployment-6b8cffdd64-slvx8   0/1     Init:0/1   0          0s
course-app-deployment-6b8cffdd64-sztwp   0/1     Init:0/1   0          0s
course-app-deployment-6b8cffdd64-zrt6z   0/1     Init:0/1   0          0s
course-app-deployment-6b8cffdd64-zttf4   0/1     Init:0/1   0          0s
```
#### По перше при зміні стратегії kubernetes автоматично не редеплоїть контейнери.
#### По друге, бачимо що всі контейнери зупиняються, а потім стартують. Тобто ми отримуємо downtime.
#### Замінимо стратегію на rollingUpdate
```
kubectl apply -f  deployment.yaml
nickdikiy@MacBook-Pro-Nick lesson-07 % kubectl rollout restart deployment -n homework
deployment.apps/course-app-deployment restarted
nickdikiy@MacBook-Pro-Nick lesson-07 % kubectl get  pods -n homework                 
NAME                                     READY   STATUS            RESTARTS   AGE
course-app-deployment-6674487dff-jtpqc   0/1     PodInitializing   0          2s
course-app-deployment-6674487dff-tbcbf   0/1     PodInitializing   0          2s
course-app-deployment-67776ff48c-428j4   1/1     Running           0          31s
course-app-deployment-67776ff48c-54pbn   1/1     Running           0          28s
course-app-deployment-67776ff48c-8hzjl   1/1     Running           0          25s
course-app-deployment-67776ff48c-8m8t9   1/1     Running           0          25s
course-app-deployment-67776ff48c-gjm9c   1/1     Running           0          31s
course-app-deployment-67776ff48c-lctqg   1/1     Running           0          28s
course-app-deployment-67776ff48c-tc9wp   1/1     Running           0          31s
course-app-deployment-67776ff48c-w25p6   1/1     Running           0          31s
course-app-deployment-67776ff48c-whrh2   1/1     Running           0          28s

nickdikiy@MacBook-Pro-Nick lesson-07 % kubectl get  pods -n homework
NAME                                     READY   STATUS            RESTARTS   AGE
course-app-deployment-6674487dff-fgcn8   0/1     PodInitializing   0          3s
course-app-deployment-6674487dff-jfj4d   0/1     PodInitializing   0          3s
course-app-deployment-6674487dff-jtpqc   1/1     Running           0          5s
course-app-deployment-6674487dff-tbcbf   1/1     Running           0          5s
course-app-deployment-67776ff48c-428j4   1/1     Running           0          34s
course-app-deployment-67776ff48c-54pbn   1/1     Running           0          31s
course-app-deployment-67776ff48c-8hzjl   1/1     Running           0          28s
course-app-deployment-67776ff48c-8m8t9   1/1     Running           0          28s
course-app-deployment-67776ff48c-tc9wp   1/1     Running           0          34s
course-app-deployment-67776ff48c-w25p6   1/1     Running           0          34s
course-app-deployment-67776ff48c-whrh2   1/1     Running           0          31s

nickdikiy@MacBook-Pro-Nick lesson-07 % kubectl get  pods -n homework
NAME                                     READY   STATUS     RESTARTS   AGE
course-app-deployment-6674487dff-fgcn8   1/1     Running    0          5s
course-app-deployment-6674487dff-hzbzk   0/1     Init:0/1   0          2s
course-app-deployment-6674487dff-jfj4d   1/1     Running    0          5s
course-app-deployment-6674487dff-jtpqc   1/1     Running    0          7s
course-app-deployment-6674487dff-tbcbf   1/1     Running    0          7s
course-app-deployment-6674487dff-zx2fs   0/1     Init:0/1   0          2s
course-app-deployment-67776ff48c-54pbn   1/1     Running    0          33s
course-app-deployment-67776ff48c-8hzjl   1/1     Running    0          30s
course-app-deployment-67776ff48c-8m8t9   1/1     Running    0          30s
course-app-deployment-67776ff48c-w25p6   1/1     Running    0          36s
course-app-deployment-67776ff48c-whrh2   1/1     Running    0          33s

nickdikiy@MacBook-Pro-Nick lesson-07 % kubectl get  pods -n homework
NAME                                     READY   STATUS    RESTARTS   AGE
course-app-deployment-6674487dff-fgcn8   1/1     Running   0          18s
course-app-deployment-6674487dff-hzbzk   1/1     Running   0          15s
course-app-deployment-6674487dff-jfj4d   1/1     Running   0          18s
course-app-deployment-6674487dff-jtpqc   1/1     Running   0          20s
course-app-deployment-6674487dff-l6dhm   1/1     Running   0          8s
course-app-deployment-6674487dff-lqx6x   1/1     Running   0          8s
course-app-deployment-6674487dff-lzqhg   1/1     Running   0          11s
course-app-deployment-6674487dff-q7n4b   1/1     Running   0          11s
course-app-deployment-6674487dff-tbcbf   1/1     Running   0          20s
course-app-deployment-6674487dff-zx2fs   1/1     Running   0          15s
```

#### По подам видно що контейнери перестворюються поступово, відповідно downtime ми не отримаємо. При цьому архітектура додатку має дозволяти такий тип деплою.
