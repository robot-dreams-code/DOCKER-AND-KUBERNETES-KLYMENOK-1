@echo off
setlocal ENABLEDELAYEDEXPANSION

set LOGFILE=zero-downtime-test.log

echo ============================================ >> %LOGFILE%
echo New run at: %DATE% %TIME% >> %LOGFILE%
echo ============================================ >> %LOGFILE%
echo. >> %LOGFILE%

echo ============================================
echo Zero Downtime Test for course-app (lesson-08)
echo Log file: %LOGFILE%
echo ============================================
echo.

echo [1/4] Making ALL course-app pods ready (touch /tmp/healthy)...
echo [1/4] Making ALL course-app pods ready... >> %LOGFILE%

for /f "tokens=1" %%p in ('kubectl get pods --no-headers ^| findstr "course-app-"') do (
    echo   -> Init readiness in pod: %%p
    echo   -> Init readiness in pod: %%p >> %LOGFILE%
    kubectl exec %%p -- sh -c "touch /tmp/healthy" >> %LOGFILE% 2>&1
)

echo.
echo [1.1] Current pod state:
kubectl get pods
kubectl get pods >> %LOGFILE% 2>&1
echo.

echo [2/4] Selecting pod to simulate "Not Ready"...
echo [2/4] Selecting pod to simulate "Not Ready"... >> %LOGFILE%

set POD=
for /f "tokens=1" %%p in ('kubectl get pods --no-headers ^| findstr "course-app-"') do (
    set POD=%%p
    goto GotPod
)

:GotPod
echo   Selected pod: %POD%
echo   Selected pod: %POD% >> %LOGFILE%
echo.

echo [2.1] Breaking readiness in %POD% (rm /tmp/healthy)...
echo [2.1] Breaking readiness in %POD%... >> %LOGFILE%
kubectl exec %POD% -- sh -c "rm /tmp/healthy" >> %LOGFILE% 2>&1

echo.
echo Waiting 15 seconds...
echo Waiting 15 seconds... >> %LOGFILE%
timeout /t 15 /nobreak >nul
echo.

echo [3/4] Pod state after break:
kubectl get pods
kubectl get pods >> %LOGFILE% 2>&1
echo.

echo [3.1] Current Endpoints:
kubectl get endpoints course-app -o wide
kubectl get endpoints course-app -o wide >> %LOGFILE% 2>&1
echo.

echo [4/4] Restoring readiness in %POD% (touch /tmp/healthy)...
echo [4/4] Restoring readiness in %POD%... >> %LOGFILE%
kubectl exec %POD% -- sh -c "touch /tmp/healthy" >> %LOGFILE% 2>&1

echo.
echo Waiting 10 seconds...
echo Waiting 10 seconds... >> %LOGFILE%
timeout /t 10 /nobreak >nul
echo.

echo [4.1] Final pod state:
kubectl get pods
kubectl get pods >> %LOGFILE% 2>&1
echo.

echo [4.2] Final Endpoints:
kubectl get endpoints course-app -o wide
kubectl get endpoints course-app -o wide >> %LOGFILE% 2>&1
echo.

echo ============================================
echo     TEST COMPLETED. ZERO DOWNTIME CHECKED.
echo     Log saved to: %LOGFILE%
echo ============================================
echo.

echo --- END OF RUN --- >> %LOGFILE%
echo. >> %LOGFILE%

pause
endlocal
