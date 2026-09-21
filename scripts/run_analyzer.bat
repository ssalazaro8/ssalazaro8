@echo off
REM GitHub Profile Analyzer - Windows Batch Script

setlocal enabledelayedexpansion

echo.
echo ==========================================
echo   GitHub Profile Statistics Analyzer
echo ==========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    echo and make sure it's added to your PATH
    pause
    exit /b 1
)

echo [INFO] Python found:
python --version

REM Check if GitHub CLI is installed
gh --version >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo [WARNING] GitHub CLI (gh) is not installed
    echo [INFO] Install it from: https://cli.github.com/
    echo [INFO] Or via Chocolatey: choco install gh
    echo.
    pause
    exit /b 1
)

echo [INFO] GitHub CLI found:
gh --version

REM Run the analyzer
echo.
echo [INFO] Running analyzer...
echo ==========================================
echo.

cd /d "%~dp0"
python analyzer.py

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo [SUCCESS] Statistics updated successfully!
    echo [INFO] Open ../index.html to view the dashboard
    echo ==========================================
) else (
    echo.
    echo [ERROR] Analyzer failed with exit code: %errorlevel%
)

echo.
pause
