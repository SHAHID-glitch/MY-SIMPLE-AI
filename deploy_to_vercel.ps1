# Vercel Deployment Helper Script
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Vercel Deployment Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Vercel CLI is installed
$vercelInstalled = Get-Command vercel -ErrorAction SilentlyContinue
if (-not $vercelInstalled) {
    Write-Host "[ERROR] Vercel CLI is not installed!" -ForegroundColor Red
    Write-Host ""
    Write-Host "Please install it first:" -ForegroundColor Yellow
    Write-Host "  npm install -g vercel" -ForegroundColor White
    Write-Host ""
    Write-Host "Or use the web deployment method:" -ForegroundColor Yellow
    Write-Host "  https://vercel.com/new" -ForegroundColor White
    Write-Host ""
    Read-Host "Press Enter to exit"
    exit 1
}

# Check authentication
Write-Host "[1/3] Checking Vercel authentication..." -ForegroundColor Yellow
$whoami = vercel whoami 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "Please login to Vercel:" -ForegroundColor Yellow
    vercel login
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Login failed!" -ForegroundColor Red
        Read-Host "Press Enter to exit"
        exit 1
    }
}

# Deploy
Write-Host ""
Write-Host "[2/3] Deploying to Vercel..." -ForegroundColor Yellow
Write-Host ""
vercel --prod

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "   Deployment Successful! 🎉" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "[NEXT STEPS]" -ForegroundColor Cyan
    Write-Host "1. Add your GOOGLE_API_KEY environment variable:" -ForegroundColor White
    Write-Host "   vercel env add GOOGLE_API_KEY" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "2. Redeploy to apply the environment variable:" -ForegroundColor White
    Write-Host "   vercel --prod" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "3. Visit your live site!" -ForegroundColor White
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "[ERROR] Deployment failed!" -ForegroundColor Red
    Write-Host "Please check the error messages above." -ForegroundColor Yellow
    Write-Host ""
}

Read-Host "Press Enter to exit"
