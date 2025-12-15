### Розширені можливості Kubernetes. Контролери та оператори

Встановлюємо оператор командою, наданою розробником

```
# Install the CRD and Operator
kubectl apply -f https://raw.githubusercontent.com/dragonflydb/dragonfly-operator/main/manifests/dragonfly-operator.yaml
```
Перевірка:
```
$ kubectl get pods -n dragonfly-operator-system
NAME                                                    READY   STATUS    RESTARTS   AGE
dragonfly-operator-controller-manager-97cdfcc85-slqfd   2/2     Running   0          8m16s
```
Підмінюємо хост в values.yaml хелм-чарта. Інсталюємо чарт, перевіряємо результат:
![1](images/hw_12_1.png)


Файл для ролі створений за допомогою статті https://spacelift.io/blog/kubernetes-rbac та ШІ.
Вивід команд перевірки:
```
Arsen@DESKTOP-G8LOPU1 MINGW64 /d/Dev projects/DOCKER-AND-KUBERNETES-KLYMENOK/homeworks/bakhtishaiev/module-4/lesson-12 (bakhtishaiev_a_hw_module4_lesson12)
$ kubectl auth can-i list dragonflies -n course-app   --as=system:serviceaccount:course-app:db-viewer
yes

Arsen@DESKTOP-G8LOPU1 MINGW64 /d/Dev projects/DOCKER-AND-KUBERNETES-KLYMENOK/homeworks/bakhtishaiev/module-4/lesson-12 (bakhtishaiev_a_hw_module4_lesson12)
$ kubectl auth can-i delete dragonflies -n course-app  --as=system:serviceaccount:course-app:db-viewer
no

```