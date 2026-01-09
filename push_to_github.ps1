# GitHub Push Automation Script
# This script will help you push your project to GitHub

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  GEMINI AI - GitHub Deployment Script" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if Git is installed
Write-Host "Checking Git installation..." -ForegroundColor Yellow
$gitVersion = git --version 2>$null
if ($LASTEXITCODE -ne 0) {
    Write-Host "❌ Git is not installed!" -ForegroundColor Red
    Write-Host "Please install Git from: https://git-scm.com/downloads" -ForegroundColor Yellow
    exit
}
Write-Host "✅ Git is installed: $gitVersion" -ForegroundColor Green
Write-Host ""

# Initialize Git repository
Write-Host "Initializing Git repository..." -ForegroundColor Yellow
git init
Write-Host "✅ Git repository initialized" -ForegroundColor Green
Write-Host ""

# Configure Git user
Write-Host "Configuring Git user..." -ForegroundColor Yellow
$username = Read-Host "Enter your GitHub username (default: SHAHID-glitch)"
if ([string]::IsNullOrWhiteSpace($username)) {
    $username = "SHAHID-glitch"
}

$email = Read-Host "Enter your email address"
if ([string]::IsNullOrWhiteSpace($email)) {
    Write-Host "❌ Email is required!" -ForegroundColor Red
    exit
}

git config user.name "$username"
git config user.email "$email"
Write-Host "✅ Git user configured" -ForegroundColor Green
Write-Host ""

# Add all files
Write-Host "Adding files to Git..." -ForegroundColor Yellow
git add .
Write-Host "✅ All files added" -ForegroundColor Green
Write-Host ""

# Show status
Write-Host "Git Status:" -ForegroundColor Yellow
git status --short
Write-Host ""

# Create commit
Write-Host "Creating commit..." -ForegroundColor Yellow
$commitMessage = Read-Host "Enter commit message (default: 🎨 Initial commit: 3D Gemini AI Assistant)"
if ([string]::IsNullOrWhiteSpace($commitMessage)) {
    $commitMessage = "🎨 Initial commit: 3D Gemini AI Assistant with glassmorphism UI"
}

git commit -m "$commitMessage"
Write-Host "✅ Commit created" -ForegroundColor Green
Write-Host ""

# Repository name
$repoName = Read-Host "Enter repository name (default: MY-SIMPLE-AI)"
if ([string]::IsNullOrWhiteSpace($repoName)) {
    $repoName = "MY-SIMPLE-AI"
}

# Add remote origin
Write-Host "Adding remote origin..." -ForegroundColor Yellow
$remoteUrl = "https://github.com/$username/$repoName.git"
git remote remove origin 2>$null
git remote add origin $remoteUrl
Write-Host "✅ Remote origin added: $remoteUrl" -ForegroundColor Green
Write-Host ""

# Rename branch to main
Write-Host "Renaming branch to 'main'..." -ForegroundColor Yellow
git branch -M main
Write-Host "✅ Branch renamed to 'main'" -ForegroundColor Green
Write-Host ""

# Push to GitHub
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  Ready to Push to GitHub!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "IMPORTANT: You need to create the repository on GitHub first!" -ForegroundColor Yellow
Write-Host "1. Go to: https://github.com/$username" -ForegroundColor Cyan
Write-Host "2. Click 'New' to create a repository" -ForegroundColor Cyan
Write-Host "3. Name it: $repoName" -ForegroundColor Cyan
Write-Host "4. DO NOT initialize with README" -ForegroundColor Red
Write-Host "5. Click 'Create repository'" -ForegroundColor Cyan
Write-Host ""

$continue = Read-Host "Have you created the repository? (y/n)"
if ($continue -ne "y" -and $continue -ne "Y") {
    Write-Host "Please create the repository first and run this script again." -ForegroundColor Yellow
    exit
}

Write-Host ""
Write-Host "Pushing to GitHub..." -ForegroundColor Yellow
Write-Host "You will be prompted for credentials:" -ForegroundColor Yellow
Write-Host "  Username: $username" -ForegroundColor Cyan
Write-Host "  Password: Use your Personal Access Token (NOT your password)" -ForegroundColor Red
Write-Host ""
Write-Host "Don't have a token? Get one here:" -ForegroundColor Yellow
Write-Host "https://github.com/settings/tokens/new" -ForegroundColor Cyan
Write-Host ""

git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Green
    Write-Host "  ✅ SUCCESS!" -ForegroundColor Green
    Write-Host "========================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your project is now on GitHub! 🎉" -ForegroundColor Green
    Write-Host ""
    Write-Host "View it at:" -ForegroundColor Cyan
    Write-Host "https://github.com/$username/$repoName" -ForegroundColor Cyan
    Write-Host ""
} else {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Red
    Write-Host "  ❌ PUSH FAILED" -ForegroundColor Red
    Write-Host "========================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Repository doesn't exist on GitHub" -ForegroundColor Cyan
    Write-Host "2. Wrong credentials (use Personal Access Token)" -ForegroundColor Cyan
    Write-Host "3. No internet connection" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Check the GITHUB_DEPLOYMENT_GUIDE.md for help" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to exit..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
