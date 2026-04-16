@echo off
echo [1/2] Killing process on port 8000...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr ":8000 " ^| findstr "LISTENING"') do (
    echo Killing PID %%a
    taskkill /PID %%a /F >nul 2>&1
)

echo [2/2] Starting server...
call .venv\Scripts\activate
python main.py
