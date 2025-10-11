# LinkedIn Job Application Automation MVP - Environment Setup
# PowerShell script to set environment variables

Write-Host "Setting up LinkedIn automation environment variables..." -ForegroundColor Green

# Set LinkedIn credentials (replace with your actual credentials)
$env:LINKEDIN_EMAIL = "your-email@example.com"
$env:LINKEDIN_PASSWORD = "your-password-here"

# Set job search settings
$env:JOB_KEYWORDS = "Data Analyst,Business Analyst,Data Scientist"
$env:EASY_APPLY_ONLY = "true"
$env:MAX_APPLICATIONS_PER_DAY = "10"

# Set browser settings
$env:HEADLESS = "false"
$env:IMPLICIT_WAIT = "10"
$env:PAGE_LOAD_TIMEOUT = "30"

Write-Host "Environment variables set successfully!" -ForegroundColor Green
Write-Host "You can now run: python main.py" -ForegroundColor Yellow

# Display current settings
Write-Host "`nCurrent Configuration:" -ForegroundColor Cyan
Write-Host "  Email: $env:LINKEDIN_EMAIL"
Write-Host "  Job Keywords: $env:JOB_KEYWORDS"
Write-Host "  Easy Apply Only: $env:EASY_APPLY_ONLY"
Write-Host "  Max Applications/Day: $env:MAX_APPLICATIONS_PER_DAY"
Write-Host "  Headless Mode: $env:HEADLESS"
