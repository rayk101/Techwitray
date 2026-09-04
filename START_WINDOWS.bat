@echo off
cd /d "%~dp0"
py -3 -c "import sys; assert sys.version_info >= (3, 11)" >nul 2>&1
if not errorlevel 1 (
    py -3 start.py
    pause
    exit /b
)
python -c "import sys; assert sys.version_info >= (3, 11)" >nul 2>&1
if not errorlevel 1 (
    python start.py
    pause
    exit /b
)
echo Please install Python 3.11 or newer from https://www.python.org/downloads/
echo Then open this file again.
pause
