Отже, мені на диво легко все вдалося (конкретно імплементація). Шукати як пишеться yaml довелося використовуючи пошук в документації
Не можна просто так взяти і відразу почати писати конфіг. Спочатку доки накидують тону теорії.

Отже спочатку я перевірив шо там той ранчер мені встановив і шо в мене є. Ну і звісно я зробив alias k="kubectl"
Перевірив які є контексти в ранчера (там тільки один)
kubectl config get-contexts

Подивився на ноди
kubectl get nodes

Беручи за зразок приклади з доків написав конфіги і перевірив їх
kubectl apply --dry-run=client -f <file>.yaml
kubectl apply --dry-run=server -f <file>.yaml

В мене була там помилка з відступами (табами) (пробілами), то клієнт нічого не видав, а от сервер вказав на помилку

Деплоїв я вот так все відразу 
kubectl apply -f .

І видаляв так само 
kubectl delete -f .

Поміняв кількість реплік і перевірив зміни
Перевірив зміни kubectl diff -f <file>.yaml

І передеплоїв
kubectl apply -f deployment.yaml

kubectl rollout status deployment snak-app-deployment 
повернув
deployment "snak-app-deployment" successfully rolled out

NAME                  READY   UP-TO-DATE   AVAILABLE   AGE
snak-app-deployment   10/10   10           10          4m57s

Всі 10 реплік реді ту го (скрін запущеної апки в папці)

Додаткові команди які використовував

kubectl get deployments
kubectl get pods
kubectl get pods -o wide
kubectl get svc
kubectl get endpoints <service>
kubectl logs <pod-name>
kubectl rollout history deployment <name>
