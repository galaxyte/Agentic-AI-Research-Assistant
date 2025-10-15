@echo off
REM Agentic AI Research Assistant - Setup Script for Windows
REM This script automates the initial setup process

echo ========================================
echo Agentic AI Research Assistant - Setup
echo ========================================
echo.

REM Check Python
echo [*] Checking Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [X] Python is not installed. Please install Python 3.9 or higher.
    pause
    exit /b 1
)
echo [+] Python found
echo.

REM Check Node.js
echo [*] Checking Node.js...
node --version >nul 2>&1
if errorlevel 1 (
    echo [X] Node.js is not installed. Please install Node.js 18 or higher.
    pause
    exit /b 1
)
echo [+] Node.js found
echo.

REM Check npm
echo [*] Checking npm...
npm --version >nul 2>&1
if errorlevel 1 (
    echo [X] npm is not installed. Please install npm.
    pause
    exit /b 1
)
echo [+] npm found
echo.

REM Backend setup
echo ========================================
echo Setting up Backend...
echo ========================================
cd backend

REM Create virtual environment
if not exist "venv" (
    echo [*] Creating Python virtual environment...
    python -m venv venv
    echo [+] Virtual environment created
) else (
    echo [!] Virtual environment already exists
)

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [X] Failed to activate virtual environment
    pause
    exit /b 1
)
echo [+] Virtual environment activated

REM Install dependencies
echo [*] Installing Python dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt >nul 2>&1
echo [+] Python dependencies installed

REM Setup environment file
if not exist ".env" (
    echo [*] Creating .env file...
    copy .env.example .env >nul
    echo [!] Please edit backend\.env and add your API keys:
    echo     - OPENAI_API_KEY
    echo     - TAVILY_API_KEY
) else (
    echo [!] .env file already exists
)

cd ..
echo.

REM Frontend setup
echo ========================================
echo Setting up Frontend...
echo ========================================
cd frontend

REM Install dependencies
echo [*] Installing Node.js dependencies...
call npm install >nul 2>&1
echo [+] Node.js dependencies installed

cd ..
echo.

REM Docker check (optional)
echo ========================================
echo Checking for Docker (optional)...
echo ========================================
docker --version >nul 2>&1
if errorlevel 1 (
    echo [!] Docker not found. Install it for containerized deployment.
) else (
    echo [+] Docker found
    docker-compose --version >nul 2>&1
    if errorlevel 1 (
        echo [!] Docker Compose not found. Install it for easy deployment.
    ) else (
        echo [+] Docker Compose found
        echo [*] You can use 'docker-compose up' to start all services
    )
)
echo.

REM Summary
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo.
echo 1. Configure your API keys:
echo    Edit: backend\.env
echo    Required: OPENAI_API_KEY, TAVILY_API_KEY
echo.
echo 2. Start the backend:
echo    cd backend
echo    venv\Scripts\activate
echo    python main.py
echo.
echo 3. In a new terminal, start the frontend:
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open your browser:
echo    http://localhost:3000
echo.
echo Or use Docker (if installed):
echo    docker-compose up
echo.
echo For more information, see README.md or QUICKSTART.md
echo.
echo Happy researching!
echo.
pause

