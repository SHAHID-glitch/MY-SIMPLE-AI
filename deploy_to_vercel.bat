@echo off
echo ========================================
echo   Vercel Deployment Helper
echo ========================================
echo.

REM Check if Vercel CLI is installed
where vercel >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo [ERROR] Vercel CLI is not installed!
    echo.
    echo Please install it first:
    echo   npm install -g vercel
    echo.
    echo Or use the web deployment method:
    echo   https://vercel.com/new
    echo.
    pause
    exit /b 1
)

echo [1/3] Checking Vercel authentication...
vercel whoami
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Please login to Vercel:
    vercel login
    if %ERRORLEVEL% NEQ 0 (
        echo [ERROR] Login failed!
        pause
        exit /b 1
    )
)

echo.
echo [2/3] Deploying to Vercel...
echo.
vercel --prod

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ========================================
    echo   Deployment Successful! 🎉
    echo ========================================
    echo.
    echo [NEXT STEPS]
    echo 1. Add your GOOGLE_API_KEY environment variable:
    echo    vercel env add GOOGLE_API_KEY
    echo.
    echo 2. Redeploy to apply the environment variable:
    echo    vercel --prod
    echo.
    echo 3. Visit your live site!
    echo.
) else (
    echo.
    echo [ERROR] Deployment failed!
    echo Please check the error messages above.
    echo.
)

pause
