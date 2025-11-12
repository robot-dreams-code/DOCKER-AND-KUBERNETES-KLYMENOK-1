# module-02/lesson-03 – vi.petrushenko

**Go додаток** `apps/simple-app`  
Multi-stage → **19 MB**  
Нерут-користувач `appuser` (uid 1001)  
EXPOSE 8080  

**Образ на Docker Hub:**  
https://hub.docker.com/r/vvpet/simple-app  

**Запуск з будь-якого комп'ютера:**
```bash
docker run -p 8080:8080 vvpet/simple-app:latest
