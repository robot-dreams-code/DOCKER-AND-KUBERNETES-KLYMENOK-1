```console
899be1aedc09   lesson-05-app "uvicorn src.main:ap…"   34 seconds ago      Up 23 seconds (healthy)   0.0.0.0:8080->8080/tcp, [::]:8080->8080/tcp  lesson-05-app-1
8978757bf88a   redis:7-alpine "docker-entrypoint.s…"   34 seconds ago      Up 33 seconds (healthy)   6379/tcp                                  lesson-05-redis-1
```
Були нюанси з використанням localhost для хелзчеку пітон апки. Поміняв на 127.0.0.1 і все запрацювало, сервіс позначається як хелзі.

Надибав таку команду, щоб дістати результати хелзчеків
docker inspect --format='{{json .State.Health}}' container | jq
```
{
  "Status": "healthy",
  "FailingStreak": 0,
  "Log": [
    {
      "Start": "2025-11-16T23:07:14.13172032+02:00",
      "End": "2025-11-16T23:07:14.206132528+02:00",
      "ExitCode": 0,
      "Output": "Connecting to 127.0.0.1:8080 (127.0.0.1:8080)\nremote file exists\n"
    },
    {
      "Start": "2025-11-16T23:07:19.215976864+02:00",
      "End": "2025-11-16T23:07:19.279723281+02:00",
      "ExitCode": 0,
      "Output": "Connecting to 127.0.0.1:8080 (127.0.0.1:8080)\nremote file exists\n"
    },
    {
      "Start": "2025-11-16T23:07:24.280858908+02:00",
      "End": "2025-11-16T23:07:24.341379158+02:00",
      "ExitCode": 0,
      "Output": "Connecting to 127.0.0.1:8080 (127.0.0.1:8080)\nremote file exists\n"
    },
    {
      "Start": "2025-11-16T23:07:29.341877035+02:00",
      "End": "2025-11-16T23:07:29.426705077+02:00",
      "ExitCode": 0,
      "Output": "Connecting to 127.0.0.1:8080 (127.0.0.1:8080)\nremote file exists\n"
    },
    {
      "Start": "2025-11-16T23:07:34.430604579+02:00",
      "End": "2025-11-16T23:07:34.508218163+02:00",
      "ExitCode": 0,
      "Output": "Connecting to 127.0.0.1:8080 (127.0.0.1:8080)\nremote file exists\n"
    }
  ]
}
```

Протестив роботу вольюма. Накляцав візітів, зробив docker compose down -v і без -v. Якщо вольюми не дропати, то візити зберігаються)

SWAAAAAAARM

Заінітів вот так 
docker swarm init --advertise-addr 127.0.0.1

Я не пушив імедж в репозиторій, я просто збілдив локально і засетив в докер композ (docker-compose-swarm.yml)

Далі задеплоїв 
docker stack deploy -c stack.yml lesson05

Подивився інфу
docker stack ls
docker stack services lesson05

Там була лише одна репліка, тому я заранив
docker service scale lesson05_app=3

І воно не спрацювало. Я трохи побавився, шоб запустити в інгрес моді. Але як мені сказала АІшка

The real issue here is that **Rancher Desktop's Docker Swarm implementation doesn't properly expose ingress ports when using overlay networks** (this is a known limitation with Lima-based Docker setups)

Типу, воно все працює, все запускається, репліки раняться. Але я не можу з локалі достукатися до апки. Не еспоузиться порт нормально в інгрес моді
А, ну і + прекол з env змінними, про який я написав в слеку
