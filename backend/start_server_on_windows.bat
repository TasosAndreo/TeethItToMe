@echo off
setlocal
title Teeth It To Me - FastAPI Server

REM Move to the backend directory containing this script
cd /d "%~dp0"

echo ==========================================
echo       Teeth It To Me - Backend Server
echo ==========================================
echo.

REM Activate the virtual environment in this directory
if not exist "venv\Scripts\activate.bat" (
    echo ERROR: Virtual environment not found.
    echo Expected location: %~dp0venv\Scripts\activate.bat
    pause
    exit /b 1
)

call "venv\Scripts\activate.bat"

echo Python environment activated.
echo.
echo Starting Uvicorn at http://127.0.0.1:8000
echo Press CTRL+C to stop the server.
echo.

python -m uvicorn main:app --reload

echo.
echo Uvicorn has stopped.
pause