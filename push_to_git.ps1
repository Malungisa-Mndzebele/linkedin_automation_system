# LinkedIn Job Application Automation - Git Push Script
# PowerShell script to push repository to Git

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "LinkedIn Job Application Automation - Git Repository Push" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if git is installed
try {
    git --version | Out-Null
    Write-Host "[OK] Git is installed" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Git is not installed. Please install Git first." -ForegroundColor Red
    Write-Host "Download from: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Yellow
Write-Host "IMPORTANT: Security Check" -ForegroundColor Yellow
Write-Host "======================================================================" -ForegroundColor Yellow
Write-Host "Before pushing, ensure that:" -ForegroundColor Yellow
Write-Host "  [X] All log files are removed or ignored" -ForegroundColor White
Write-Host "  [X] Database files are removed or ignored" -ForegroundColor White
Write-Host "  [X] config.json contains only example data" -ForegroundColor White
Write-Host "  [X] No hardcoded credentials in code" -ForegroundColor White
Write-Host ""

$continue = Read-Host "Have you verified the above? (yes/no)"
if ($continue -ne "yes") {
    Write-Host "[INFO] Push cancelled. Please verify security before pushing." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Git Repository Setup" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Check if .git exists
if (Test-Path ".git") {
    Write-Host "[INFO] Git repository already initialized" -ForegroundColor Green
} else {
    Write-Host "[INFO] Initializing new git repository..." -ForegroundColor Yellow
    git init
    Write-Host "[OK] Git repository initialized" -ForegroundColor Green
}

Write-Host ""
Write-Host "Enter your repository URL (e.g., https://github.com/username/repo.git):" -ForegroundColor Cyan
$repoUrl = Read-Host "Repository URL"

if ([string]::IsNullOrWhiteSpace($repoUrl)) {
    Write-Host "[ERROR] Repository URL is required" -ForegroundColor Red
    exit 1
}

# Check if remote exists
$remoteExists = git remote get-url origin 2>$null
if ($remoteExists) {
    Write-Host "[INFO] Remote 'origin' already exists: $remoteExists" -ForegroundColor Yellow
    $updateRemote = Read-Host "Update remote URL? (yes/no)"
    if ($updateRemote -eq "yes") {
        git remote remove origin
        git remote add origin $repoUrl
        Write-Host "[OK] Remote URL updated" -ForegroundColor Green
    }
} else {
    git remote add origin $repoUrl
    Write-Host "[OK] Remote 'origin' added" -ForegroundColor Green
}

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Adding Files" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

git add .
Write-Host "[OK] Files staged for commit" -ForegroundColor Green

Write-Host ""
Write-Host "Files to be committed:" -ForegroundColor Yellow
git diff --staged --name-status

Write-Host ""
$commitMsg = Read-Host "Enter commit message (or press Enter for default)"
if ([string]::IsNullOrWhiteSpace($commitMsg)) {
    $commitMsg = "Initial commit: LinkedIn Job Application Automation - All sensitive information removed"
}

git commit -m $commitMsg
Write-Host "[OK] Changes committed" -ForegroundColor Green

Write-Host ""
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Pushing to Repository" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

git branch -M main
Write-Host "[INFO] Branch set to 'main'" -ForegroundColor Yellow

Write-Host ""
Write-Host "[INFO] Pushing to remote repository..." -ForegroundColor Yellow
git push -u origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host "SUCCESS! Repository Pushed Successfully" -ForegroundColor Green
    Write-Host "======================================================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Your repository is now available at:" -ForegroundColor Cyan
    Write-Host "$repoUrl" -ForegroundColor White
    Write-Host ""
    Write-Host "Next steps:" -ForegroundColor Yellow
    Write-Host "1. Visit your repository online" -ForegroundColor White
    Write-Host "2. Verify no sensitive data is visible" -ForegroundColor White
    Write-Host "3. Add a repository description" -ForegroundColor White
    Write-Host "4. Configure repository settings" -ForegroundColor White
} else {
    Write-Host ""
    Write-Host "======================================================================" -ForegroundColor Red
    Write-Host "Push Failed" -ForegroundColor Red
    Write-Host "======================================================================" -ForegroundColor Red
    Write-Host ""
    Write-Host "Common issues:" -ForegroundColor Yellow
    Write-Host "1. Authentication failed - check your credentials" -ForegroundColor White
    Write-Host "2. Remote repository doesn't exist - create it first" -ForegroundColor White
    Write-Host "3. Push rejected - pull changes first with: git pull origin main" -ForegroundColor White
    Write-Host ""
    Write-Host "For help, see GIT_PUSH_INSTRUCTIONS.md" -ForegroundColor Cyan
}

Write-Host ""
Read-Host "Press Enter to exit"
