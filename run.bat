@echo off
echo Starting WELL v2 Building Management Dashboard...
echo.

if not exist venv (
    echo Virtual environment not found. Please run setup.bat first.
    pause
    exit /b 1
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Starting Flask application...
python app.py

pause