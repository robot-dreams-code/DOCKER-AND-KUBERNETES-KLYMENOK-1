@echo off
setlocal enabledelayedexpansion
title Docker Desktop automation demo

echo === Step 1: Run hello-world ===
docker run --rm hello-world || goto :error

echo.
echo === Step 2: Start Nginx on port 8080 ===
docker run -d --name web1 -p 8080:80 nginx:alpine || goto :error
echo Open http://localhost:8080 in your browser to check Nginx.

echo.
echo === Step 3: Start 10 Nginx containers on ports 8081..8090 ===
for /l %%i in (1,1,10) do (
  set /a PORT=8080+%%i
  echo Starting nginx-%%i on port !PORT!
  docker run -d --name nginx-%%i -p !PORT!:80 nginx:alpine
)
echo All containers started.

echo.
echo === Step 4: Show running containers ===
docker ps --format "table {{.Names}}\t{{.Ports}}"

echo.
echo === Step 5: Stop and remove all containers ===
for /f "tokens=*" %%i in ('docker ps -aq') do docker rm -f %%i
echo All containers stopped and removed.

echo.
echo Done! Press any key to exit.
pause >nul
exit /b 0

:error
echo.
echo [ERROR] Something went wrong. Check that Docker Desktop is running in Linux containers mode.
pause
exit /b 1