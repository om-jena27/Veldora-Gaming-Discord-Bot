@echo off
title Veldora Gaming Discord Bot Launcher
color 0A

echo ========================================================
echo          🎮 VELDORA GAMING DISCORD BOT LAUNCHER
echo ========================================================
echo.

cd /d "%~dp0"

IF NOT EXIST ".env" (
    IF NOT EXIST "bot\.env" (
        echo [!] No .env file found. Creating .env file...
        echo DISCORD_TOKEN=your_token_here > .env
        echo [+] Created .env file. Please add your Discord Bot Token inside .env!
        echo.
    )
)

echo [+] Checking Python installation...
python --version >nul 2>&1
IF %ERRORLEVEL% NEQ 0 (
    echo [X] Python is not installed or not added to PATH!
    echo Please install Python 3.10+ from python.org and check "Add Python to PATH".
    pause
    exit /b
)

echo [+] Installing / Verifying dependencies from bot\requirements.txt...
python -m pip install -r bot\requirements.txt >nul 2>&1

echo.
echo ========================================================
echo 🚀 STARTING VELDORA BOT... (Keep this window open)
echo ========================================================
echo.

python bot\main.py

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [X] Bot stopped with an error code %ERRORLEVEL%.
    pause
)
