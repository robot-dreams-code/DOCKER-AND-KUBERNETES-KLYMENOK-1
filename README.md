lesson-03/
│
├── Dockerfile
├── main.go
└── README.md


Використані технології
Golang — код застосунку
Docker multi-stage build — оптимізація образу
Alpine Linux — легкий runtime-образ
Non-root user — безпечний запуск контейнера

Зберіть Docker-образ:
docker build -t lesson-03 .

Запустіть контейнер:
docker run -p 8080:8080 lesson-03

Відкрити в браузері:
http://localhost:8080