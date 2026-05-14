@echo off
REM AI Social Media Automation Flask App - Setup Script
REM Windows Batch File

echo.
echo ========================================
echo AI Social Media Automation
echo Installation Setup
echo ========================================
echo.

REM Navigate to project directory
cd /d "C:\Users\SADANAND\ai-social-media-automation"

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo [1/5] Python found
echo.

REM Create virtual environment
echo [2/5] Creating virtual environment...
if exist "venv" (
    echo Virtual environment already exists
) else (
    python -m venv venv
    if %errorlevel% neq 0 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
)

REM Activate virtual environment
echo [3/5] Activating virtual environment...
call venv\Scripts\activate.bat
if %errorlevel% neq 0 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

REM Install requirements
echo [4/5] Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

REM Create .env from example
echo [5/5] Setting up environment file...
if not exist ".env" (
    copy .env.example .env
    echo.
    echo ========================================
    echo IMPORTANT: Edit your .env file!
    echo ========================================
    echo.
    echo 1. Open .env file: .env
    echo 2. Find the line: GEMINI_API_KEY=your_gemini_api_key_here
    echo 3. Replace with your actual API key from:
    echo    https://makersuite.google.com/app/apikey
    echo 4. Save the file
    echo.
) else (
    echo .env file already exists
)

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Edit .env file and add your Gemini API key
echo 2. Run: python app.py
echo 3. Open: http://127.0.0.1:5000
echo.
echo ========================================
echo.

pause
