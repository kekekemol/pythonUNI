@echo off
setlocal
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo.
    echo [HeartSense] Virtual environment not found.
    echo Create the project environment with: python -m venv .venv
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Django project...
".venv\Scripts\python.exe" manage.py check
if errorlevel 1 goto :failed

echo.
echo [2/3] Applying database migrations...
".venv\Scripts\python.exe" manage.py migrate --noinput
if errorlevel 1 goto :failed

echo.
echo [3/3] Starting HeartSense at http://127.0.0.1:8000/
echo Press CTRL+C to stop the server.
echo.
".venv\Scripts\python.exe" manage.py runserver
exit /b %errorlevel%

:failed
echo.
echo HeartSense could not start. Review the error above.
pause
exit /b 1
