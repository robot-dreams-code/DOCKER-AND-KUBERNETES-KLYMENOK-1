# Helm

## Мета: Перенести створену в попередніх домашніх завданнях інфраструктуру (App + Redis + Ingress) з "сирих" маніфестів (kubectl apply) у керований Helm-чарт

### Створення власного Helm-чарту для course-app

Створіть чарт для вашого застосунку, перенісши логіку з маніфестів попередніх занять (Deployment, Service, Ingress). Вимоги:
`helm create app-chart`
Шаблонізація: Основні параметри мають бути винесені у values.yaml (образ контейнера, тег, кількість реплік, хост Ingress)
Гнучкість: У шаблонах не повинно залишитись хардкоду, який заважав би розгорнути чарт у іншому неймспейсі чи з іншими налаштуваннями.

### Розгортання Redis через Bitnami Redis Chart

Замість написання власного StatefulSet для Redis, розгорніть базу даних, використовуючи популярний ком'юніті-чарт bitnami/redis

### Додайте відповідний репозиторій Helm

```sh
   helm repo add bitnami https://charts.bitnami.com/bitnami
   helm repo update
```

### Встановіть Redis у ваш кластер, налаштувавши необхідні параметри

`helm install app-redis bitnami/redis -namespace "mod03-less11" --create-namespace`

![Alt Text](img/app-redis.png)

You can also customize the installation by providing a values.yaml file or by setting individual parameters using the --set flag.
`--set auth.password="my-strong-password"`

## Інтеграція

Оновіть конфігурацію вашого чарту course-app (змінні оточення), щоб застосунок успішно підключався до нового інстансу Redis, розгорнутого через Bitnami
