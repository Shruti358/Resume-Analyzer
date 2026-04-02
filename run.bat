@echo off
REM Resume Analyzer - Quick Start Script for Windows
REM This script sets up and runs the modern Resume Analyzer application

echo.
echo ═══════════════════════════════════════════════════════════════
echo   📄 AI Resume Analyzer - Modern Professional UI
echo ═══════════════════════════════════════════════════════════════
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✓ Python detected
echo.

REM Check if pip is available
pip --version >nul 2>&1
if errorlevel 1 (
    echo ❌ pip is not available
    pause
    exit /b 1
)

echo ✓ pip detected
echo.

REM Install required packages
echo 📦 Installing required packages...
echo Press any key to continue with installation...
pause >nul

pip install -r requirements_modern.txt

if errorlevel 1 (
    echo ❌ Failed to install packages
    pause
    exit /b 1
)

echo.
echo ✓ All packages installed successfully!
echo.
echo ═══════════════════════════════════════════════════════════════
echo   Starting Resume Analyzer...
echo ═══════════════════════════════════════════════════════════════
echo.
echo 🚀 Application will open in your default browser
echo 📍 URL: http://localhost:8501
echo.
echo 💡 Tips:
echo    - Press Ctrl+C to stop the server
echo    - Use 'r' to rerun the app after making changes
echo    - Press 'c' to clear terminal
echo.

REM Run the application
streamlit run resume_analyzer_modern.py

pause
