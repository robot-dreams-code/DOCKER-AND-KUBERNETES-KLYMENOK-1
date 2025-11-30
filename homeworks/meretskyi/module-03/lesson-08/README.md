# homework-08


3. Ingress / 5. HTTPS
```
brew install mkcert

mkcert course-app.local 192.168.64.2

kubectl create secret tls course-app-tls \
 --cert=dev/course-app.local+1.pem \
 --key=dev/course-app.local+1-key.pem
 
kubectl get secret course-app-tls
```

```
kubectl get ingress course-app-ingress

NAME                 CLASS     HOSTS              ADDRESS        PORTS     AGE
course-app-ingress   traefik   course-app.local   192.168.64.2   80, 443   32m
---

kubectl describe ingress course-app-ingress
```

перевіряємо наявність SSL 
```
curl https://course-app.local -L
curl: (60) SSL certificate problem: unable to get local issuer certificate
...

```


4. Zero Downtime Test

Виставляємо readinessProbe
```yaml
          readinessProbe:
            exec:
              command:
                - sh
                - -c
                - 'test -f /tmp/healthy'
            initialDelaySeconds: 5
            periodSeconds: 5
```


Слідкуємо за ендпоінтами
```
kubectl get endpoints course-app-svc -o wide -w
```

Робимо поди готовими
```
for POD in $(kubectl get pods -l app=course-app -o name); do
  kubectl exec "$POD" -- sh -c 'echo ok > /tmp/healthy'
done
```

Бачимо, як поди отримують статус Ready 
І зʼявляються їх адреси в endpoints
