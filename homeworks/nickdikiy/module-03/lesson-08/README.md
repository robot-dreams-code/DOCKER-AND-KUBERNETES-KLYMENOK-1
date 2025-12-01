## 1. Запустимо k8s кластер
```bash
orb start k8s
```


## 2. Так як я використовую orbstack, мені потрібно налаштувати traefic.
Ingress Controller:
* Повинен читати Ingress ресурси, щоб знати, куди направляти трафік.
* Повинен дивитися Services і Endpoints, щоб знаходити IP Pod-ів backend.
* Якщо використовуємо HTTPS, повинен читати Secrets з TLS сертифікатами.

### Для цього опишемо в traefik.yaml ServiceAccount, RBAC, IngressClass, Deployment.
1. ServiceAccount
* Кожен Pod у Kubernetes може працювати з API кластера.
* ServiceAccount – це “користувач”, від імені якого Pod звертається до Kubernetes.
* Без спеціальної ServiceAccount Pod використовує default, який має мінімальні права.

2. RBAC (Role / ClusterRole / Binding)
* Role/ClusterRole – набір дозволів. Наприклад: “можна читати Ingress та Services у всіх namespace”
* RoleBinding/ClusterRoleBinding – прив’язка цих прав до конкретного ServiceAccount

3. IngressClass
* IngressClass – це ресурс кластерного рівня, який вказує, який Ingress Controller має обробляти конкретні Ingress ресурси.
* Поле spec.controller визначає контролер, наприклад traefik.io/ingress-controller.
* Якщо Ingress створюється з ingressClassName, Kubernetes знає, що його обробляє відповідний контролер.
* Через анотацію ingressclass.kubernetes.io/is-default-class: "true" можна задати IngressClass за замовчуванням, якщо Ingress не вказує ingressClassName.
* IngressClass не маршрутизує трафік сам, не обробляє TLS і не створює Pod-и; це робить сам Ingress Controller.

4. Deployment Traefik
* Deployment створює Pod-и з контейнером Traefik, який і є Ingress Controller.
* Контейнер Traefik використовує ServiceAccount для доступу до Kubernetes API і має аргументи для прослуховування портів (--entrypoints.web.address=:80, --entrypoints.websecure.address=:443) та підключення до Ingress ресурсів (--providers.kubernetesingress=true).
* Через Deployment можна масштабувати кількість Pod-ів Traefik, забезпечуючи балансування і відмовостійкість.


```bash
kubectl apply -f traefik.yaml 
kubectl get serviceaccount traefik-ingress-controller -n kube-system
kubectl get clusterrole traefik-ingress-controller
kubectl get clusterrolebinding traefik-ingress-controller
kubectl get ingressclass traefik
kubectl get deployment traefik -n kube-system 
 ```

 ```
serviceaccount/traefik-ingress-controller created
clusterrole.rbac.authorization.k8s.io/traefik-ingress-controller created
clusterrolebinding.rbac.authorization.k8s.io/traefik-ingress-controller created
ingressclass.networking.k8s.io/traefik created
deployment.apps/traefik created

NAME                         SECRETS   AGE
traefik-ingress-controller   0         14m

NAME                         CREATED AT
traefik-ingress-controller   2025-11-23T10:37:38Z

NAME                         ROLE                                     AGE
traefik-ingress-controller   ClusterRole/traefik-ingress-controller   15m

NAME      CONTROLLER                      PARAMETERS   AGE
traefik   traefik.io/ingress-controller   <none>       15m

NAME      READY   UP-TO-DATE   AVAILABLE   AGE
traefik   1/1     1            1           16m
```



## 3. Створимо ingress.yaml. Використовуватимемо локальний домен course-app.local.
### Також необхідно додати домен в /etc/hosts
```bash
echo "127.0.0.1   course-app.local" | sudo tee -a /etc/hosts
kubectl apply -f ingress.yaml
kubectl get ingress
```
```
NAME                 CLASS     HOSTS              ADDRESS   PORTS     AGE
course-app-ingress   traefik   course-app.local             80, 443   5s
```


## 3. Створимо service.yaml з типом ClusterIp:
```bash
kubectl apply -f service.yaml
kubectl get svc course-app-svc 
```
```
NAME             TYPE        CLUSTER-IP        EXTERNAL-IP   PORT(S)   AGE
course-app-svc   ClusterIP   192.168.194.218   <none>        80/TCP    2m2s
```



## 4. Встановимо certManager
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.0/cert-manager.crds.yaml
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.14.0/cert-manager.yaml
kubectl get crd | grep cert-manager
kubectl apply -f cluster-issuer.yaml -f ingress-cert.yaml
kubectl get secret course-app-tls
```
```
certificaterequests.cert-manager.io   2025-11-23T11:41:19Z
certificates.cert-manager.io          2025-11-23T11:41:20Z
challenges.acme.cert-manager.io       2025-11-23T11:41:20Z
clusterissuers.cert-manager.io        2025-11-23T11:41:20Z
issuers.cert-manager.io               2025-11-23T11:41:20Z
orders.acme.cert-manager.io           2025-11-23T11:41:20Z

clusterissuer.cert-manager.io/selfsigned-issuer created
certificate.cert-manager.io/course-app-tls created

NAME             TYPE                DATA   AGE
course-app-tls   kubernetes.io/tls   3      7m27s

```



5. Збільшимо кількість реплік, додамо проби, зробимо редеплой
```bash
kubectl get pods
kubectl get endpoints course-app-svc
```
```
NAME                                    READY   STATUS    RESTARTS   AGE
course-app-deployment-c7cc44c6d-bspfx   1/1     Running   0          176m
course-app-deployment-c7cc44c6d-lmgkm   1/1     Running   0          177m
course-app-deployment-c7cc44c6d-tmxcp   1/1     Running   0          177m

NAME             ENDPOINTS                                                                    AGE
course-app-svc   192.168.194.115:8080,192.168.194.116:8080,192.168.194.118:8080   4h
```
### Бачимо що поди отримують свої адреси. Тепер зімітуємо падіння контейнера:
```bash
kubectl exec -it course-app-deployment-c7cc44c6d-bspfx -- /bin/sh
kill 1

kubectl get endpoints course-app-svc  
```
```
NAME             ENDPOINTS                                   AGE
course-app-svc   192.168.194.115:8080,192.168.194.116:8080   4h1m
```
### Бачимо що IP неготового пода зник з ендпоінтів. Через деякий час контейнер буде перепіднято, і IP знову буде додано до ендпоінтів.
