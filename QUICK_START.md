# Quick Start Guide

## 1. Setup
```bash
python setup_full_project.py
```

## 2. Configuration
Copy `env_template.txt` to `.env` and fill in your details:
```bash
cp env_template.txt .env
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
