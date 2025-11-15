# Docker compose file 

## Додав healthcheck для сервісів
для цікавості та навчання були додані healthcheck для всіх сервісів, які запускуаютьсяя з docker-compose.yaml

## Додати томи та переконатися, що том appdata зберігає лічильник відвідувань між перезапусками контейнера
так, через додаток ми бачимо що після стопу таа запуску сервісів база та редіс підключаються до вже існуючих томів

## Налаштувати залежності/порядок запуску
Залежності були налаштовані ще в минулій домашній роботі, зараз лише розширив параметри, коли застосунок перевіряє не лише статус контейнера, а і його стан ( `condition` )

# Docker swarm 
 Для роботи нам необхідний репозиторій, для цього ми використаємо докер хаб.
 Нода у нас буде одна `manager` без воркерів

Також на хості (віртуальній машині) необхідно налаштувати мережу:

    firewall-cmd --add-port=2376/tcp --permanent;
    firewall-cmd --add-port=2377/tcp --permanent;
    firewall-cmd --add-port=7946/tcp --permanent;
    firewall-cmd --add-port=7946/udp --permanent;
    firewall-cmd --add-port=4789/udp --permanent;
    firewall-cmd --reload;

    systemctl restart docker;

##  Запустити Docker в swarm режимі
Для запуску Docker в  Swarm  режимі треба виконати команду 
    `docker swarm init`
Щоб подивитись ноди 
    `docker node ls`

## Задеплоїти stack
Для того щоб подивитись стек необхідно виконати 
    `docker stack ls`
Попередньо перед deploy services необхідно image загрузити на хост
    `docker pull rdlsolutions/course-app:1.0.3`
Потім запускаємо контейнери
    `docker stack deploy --with-registry-auth -c ./docker-compose.yaml test`
Подивитись сервіси в стеку "test"
    `docker stack services test`
Щоб видалити стек необхідно виконати команду
    `docker stack rm test`
Видалити сервіс 
    `docker service rm redis`