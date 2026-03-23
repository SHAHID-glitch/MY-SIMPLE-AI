@echo off
REM Hugging Face Spaces Deployment Script for Windows
REM Deploy Gemini AI Assistant to HF Spaces - Windows

setlocal enabledelayedexpansion

cls
echo.
echo ======================================================================
echo    GEMINI AI ASSISTANT - HUGGING FACE SPACES DEPLOYMENT WINDOWS
echo ======================================================================
echo.

REM Check if Python is installed
python3 --version >nul 2>&1
if errorlevel 1 (
    python --version >nul 2>&1
    if errorlevel 1 (
        echo.
        echo ERROR: Python is not installed!
        echo Please install Python from https://www.python.org/
        echo Make sure to add Python to PATH during installation.
        pause
        exit /b 1
    )
    set "PYTHON=python"
) else (
    set "PYTHON=python3"
)

echo [OK] Python found: %PYTHON%
echo.

REM Check if Git is installed
git --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Git is not installed!
    echo Please install Git from https://git-scm.com/
    pause
    exit /b 1
)

echo [OK] Git found
echo.

REM Install HF Hub if needed
echo Checking Hugging Face Hub...
%PYTHON% -c "from huggingface_hub import login" >nul 2>&1
if errorlevel 1 (
    echo Installing Hugging Face Hub...
    %PYTHON% -m pip install huggingface-hub -q
    echo [OK] Hugging Face Hub installed
) else (
    echo [OK] Hugging Face Hub is installed
)
echo.

REM Run deployment script
echo ======================================================================
echo Starting Hugging Face Spaces Deployment...
echo ======================================================================
echo.

%PYTHON% deploy_to_hf.py

if errorlevel 1 (
    echo.
    echo ERROR: Deployment failed!
    pause
    exit /b 1
)

echo.
echo ======================================================================
echo SUCCESS: Deployment script completed!
echo ======================================================================
echo.
pause
