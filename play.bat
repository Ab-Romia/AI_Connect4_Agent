@echo off
REM Connect 4 Platform Launcher for Windows

echo 🎮 Connect 4 Platform - Starting...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Error: Python is not installed or not in PATH.
    echo Please install Python 3.7 or higher from python.org
    pause
    exit /b 1
)

REM Display Python version
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✓ Python %PYTHON_VERSION% detected

REM Check if tkinter is available
python -c "import tkinter" 2>nul
if errorlevel 1 (
    echo ❌ Error: tkinter is not installed.
    echo.
    echo Please reinstall Python from python.org
    echo Make sure to check "tcl/tk and IDLE" during installation.
    pause
    exit /b 1
)

echo ✓ Tkinter available
echo.
echo 🚀 Launching Connect 4 Platform...
echo.

REM Run the platform
python Connect4Platform.py

pause
