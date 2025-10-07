"""
Setup script for LinkedIn Job Application Automation - Full Project
Automates the setup process for the complete system
"""
import os
import sys
import subprocess
import json
from pathlib import Path


def print_banner():
    """Print setup banner"""
    print("=" * 70)
    print("LinkedIn Job Application Automation - Full Project Setup")
    print("=" * 70)
    print()


def check_python_version():
    """Check if Python version is compatible"""
    print("Checking Python version...")
    if sys.version_info < (3, 8):
        print("[ERROR] Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        sys.exit(1)
    print(f"[OK] Python {sys.version.split()[0]} is compatible")


def install_dependencies():
    """Install required dependencies"""
    print("\nInstalling dependencies...")
    
    try:
        # Install core dependencies
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements_full.txt"])
        print("[OK] Dependencies installed successfully")
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] Error installing dependencies: {e}")
        print("Please install dependencies manually:")
        print("pip install -r requirements_full.txt")
        return False
    
    return True


def create_directories():
    """Create necessary directories"""
    print("\nCreating project directories...")
    
    directories = [
        "logs",
        "data",
        "templates",
        "static",
        "tests",
        "docs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(exist_ok=True)
        print(f"[OK] Created directory: {directory}")


def create_config_files():
    """Create configuration files"""
    print("\nCreating configuration files...")
    
    # Scheduler configuration
    scheduler_config = {
        "enabled": True,
        "daily_application_limit": 10,
        "optimal_times": {
            "morning": {"start": "09:00", "end": "11:00"},
            "afternoon": {"start": "14:00", "end": "16:00"},
            "evening": {"start": "19:00", "end": "21:00"}
        },
        "weekdays_only": True,
        "avoid_weekends": True,
        "timezone": "UTC",
        "random_delay_min": 30,
        "random_delay_max": 300,
        "cooldown_between_applications": 60,
        "max_session_duration": 120,
        "auto_pause_on_limit": True,
        "resume_next_day": True
    }
    
    with open("scheduler_config.json", "w") as f:
        json.dump(scheduler_config, f, indent=2)
    print("[OK] Created scheduler_config.json")
    
    # AI configuration
    ai_config = {
        "min_match_score": 70.0,
        "enable_resume_optimization": True,
        "enable_cover_letter_generation": True,
        "skill_weight": 0.4,
        "experience_weight": 0.25,
        "education_weight": 0.15,
        "location_weight": 0.1,
        "industry_weight": 0.1
    }
    
    with open("ai_config.json", "w") as f:
        json.dump(ai_config, f, indent=2)
    print("[OK] Created ai_config.json")
    
    # Dashboard configuration
    dashboard_config = {
        "host": "127.0.0.1",
        "port": 5000,
        "debug": False,
        "auto_start": True,
        "theme": "dark",
        "refresh_interval": 30
    }
    
    with open("dashboard_config.json", "w") as f:
        json.dump(dashboard_config, f, indent=2)
    print("[OK] Created dashboard_config.json")


def create_env_template():
    """Create environment template file"""
    print("\nCreating environment template...")
    
    env_template = """# LinkedIn Job Application Automation - Environment Variables
# Copy this file to .env and fill in your actual values

# LinkedIn Credentials
LINKEDIN_EMAIL=your-email@example.com
LINKEDIN_PASSWORD=your-password
LINKEDIN_PHONE=+1234567890

# Job Search Configuration
JOB_KEYWORDS=Data Analyst,Business Analyst,Data Scientist
PREFERRED_LOCATION=San Francisco, CA
MAX_APPLICATIONS_PER_DAY=10
EASY_APPLY_ONLY=true

# Experience & Skills
EXPERIENCE_YEARS=3
SKILLS=Python,SQL,Tableau,Excel,Statistics
EDUCATION=Bachelor's Degree in Computer Science
CERTIFICATIONS=Google Analytics,Tableau Desktop

# Preferences
REMOTE_PREFERENCE=true
EXPERIENCE_LEVEL=mid
COMPANY_SIZE=medium
PREFERRED_INDUSTRIES=Technology,Finance,Healthcare

# AI Configuration
AI_MATCHING_ENABLED=true
MIN_MATCH_SCORE=70.0
RESUME_OPTIMIZATION=true
COVER_LETTER_GENERATION=true

# Dashboard Configuration
DASHBOARD_ENABLED=true
DASHBOARD_HOST=127.0.0.1
DASHBOARD_PORT=5000

# Database Configuration
DATABASE_PATH=linkedin_automation.db
BACKUP_ENABLED=true
BACKUP_INTERVAL=24

# Logging Configuration
LOG_LEVEL=INFO
LOG_FILE=enhanced_automation.log
ACTION_LOG_FILE=enhanced_actions.log
"""
    
    with open(".env.template", "w") as f:
        f.write(env_template)
    print("[OK] Created .env.template")


def create_startup_scripts():
    """Create startup scripts for different platforms"""
    print("\nCreating startup scripts...")
    
    # Windows batch script
    windows_script = """@echo off
echo Starting LinkedIn Job Application Automation - Full Project
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    pause
    exit /b 1
)

REM Install dependencies if needed
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\\Scripts\\activate.bat

REM Install dependencies
pip install -r requirements_full.txt

REM Start the application
echo Starting enhanced automation...
python enhanced_main.py

pause
"""
    
    with open("start_automation.bat", "w") as f:
        f.write(windows_script)
    print("[OK] Created start_automation.bat")
    
    # Linux/Mac shell script
    unix_script = """#!/bin/bash
echo "Starting LinkedIn Job Application Automation - Full Project"
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements_full.txt

# Start the application
echo "Starting enhanced automation..."
python enhanced_main.py
"""
    
    with open("start_automation.sh", "w") as f:
        f.write(unix_script)
    
    # Make script executable
    os.chmod("start_automation.sh", 0o755)
    print("[OK] Created start_automation.sh")


def create_documentation():
    """Create basic documentation files"""
    print("\nCreating documentation...")
    
    # Quick start guide
    quick_start = """# Quick Start Guide

## 1. Setup
```bash
python setup_full_project.py
```

## 2. Configuration
Copy `.env.template` to `.env` and fill in your details:
```bash
cp .env.template .env
# Edit .env with your LinkedIn credentials and preferences
```

## 3. Run Automation
```bash
# Interactive mode
python enhanced_main.py

# Or use startup script
./start_automation.sh  # Linux/Mac
start_automation.bat   # Windows
```

## 4. Web Dashboard
```bash
python web_dashboard.py
# Open http://127.0.0.1:5000 in your browser
```

## 5. Monitor Progress
- Check the web dashboard for real-time updates
- View log files for detailed information
- Use the analytics to track your success

## Troubleshooting
- Run `python chrome_cleanup.py` if you have browser issues
- Check log files for error details
- Ensure Chrome browser is installed
"""
    
    with open("QUICK_START.md", "w") as f:
        f.write(quick_start)
    print("[OK] Created QUICK_START.md")


def run_tests():
    """Run basic tests to verify setup"""
    print("\nRunning basic tests...")
    
    try:
        # Test imports
        import selenium
        import flask
        import sqlite3
        print("[OK] Core dependencies imported successfully")
        
        # Test database creation
        from database import DatabaseManager
        db = DatabaseManager("test.db")
        print("[OK] Database system working")
        
        # Test AI matcher
        from ai_job_matcher import AIJobMatcher
        matcher = AIJobMatcher()
        print("[OK] AI matching system working")
        
        # Test scheduler
        from scheduler import AutomationScheduler
        scheduler = AutomationScheduler()
        print("[OK] Scheduler system working")
        
        # Clean up test database
        if os.path.exists("test.db"):
            os.remove("test.db")
        
        print("[OK] All systems working correctly")
        return True
        
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")
        return False


def print_completion_message():
    """Print setup completion message"""
    print("\n" + "=" * 70)
    print("[SUCCESS] Setup Complete!")
    print("=" * 70)
    print()
    print("Your LinkedIn Job Application Automation system is ready!")
    print()
    print("Next steps:")
    print("1. Copy .env.template to .env and configure your settings")
    print("2. Run: python enhanced_main.py")
    print("3. Or start the web dashboard: python web_dashboard.py")
    print()
    print("Files created:")
    print("[OK] Configuration files (scheduler_config.json, ai_config.json)")
    print("[OK] Environment template (.env.template)")
    print("[OK] Startup scripts (start_automation.bat, start_automation.sh)")
    print("[OK] Documentation (QUICK_START.md)")
    print("[OK] Project directories (logs, data, templates, etc.)")
    print()
    print("For more information, see README_FULL_PROJECT.md")
    print("=" * 70)


def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python_version()
    
    # Install dependencies
    if not install_dependencies():
        print("[ERROR] Setup failed during dependency installation")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Create configuration files
    create_config_files()
    
    # Create environment template
    create_env_template()
    
    # Create startup scripts
    create_startup_scripts()
    
    # Create documentation
    create_documentation()
    
    # Run tests
    if not run_tests():
        print("[WARNING] Setup completed with warnings - some tests failed")
        print("You may need to install additional dependencies manually")
    
    # Print completion message
    print_completion_message()


if __name__ == "__main__":
    main()
