@echo off
title GitHub Deployment - Gemini AI

echo ========================================
echo   GEMINI AI - GitHub Deployment
echo ========================================
echo.
echo Starting PowerShell script...
echo.

powershell -ExecutionPolicy Bypass -File "%~dp0push_to_github.ps1"

pause
