# LinkedIn Job Application Automation

A comprehensive, AI-powered LinkedIn job application automation system that helps you efficiently apply to relevant job opportunities with intelligent matching, database tracking, and real-time monitoring.

## 🚀 Features

### Core Automation
- **Intelligent Job Search**: Advanced job discovery with multiple search strategies
- **Smart Application Process**: Automated Easy Apply with intelligent form filling
- **LinkedIn Interface Adaptation**: Robust selectors that adapt to LinkedIn's changing interface
- **Session Management**: Proper browser session handling with cleanup

### AI-Powered Features
- **Job Matching**: AI analyzes job descriptions and matches them with your profile
- **Resume Optimization**: Suggests keywords to improve ATS compatibility
- **Smart Filtering**: Only applies to jobs that match your criteria
- **Cover Letter Generation**: AI-generated personalized cover letters

### Database & Analytics
- **Application Tracking**: Complete database of all applications and responses
- **Analytics Dashboard**: Comprehensive statistics and success metrics
- **Job History**: Track application status, interviews, and outcomes
- **Performance Metrics**: Success rates, response times, and trends

### Web Dashboard
- **Real-time Monitoring**: Live view of automation progress
- **Control Panel**: Start, stop, pause, and resume automation
- **Analytics Visualization**: Interactive charts and graphs
- **Configuration Management**: Update settings through web interface

### Advanced Scheduling
- **Optimal Timing**: Applies during best times for maximum visibility
- **Daily Limits**: Respects LinkedIn's application limits
- **Smart Pausing**: Automatically pauses when limits are reached
- **Session Management**: Tracks and manages automation sessions

## 📁 Project Structure

```
linkedin-automation/
├── 📁 logs/                           # Log files directory
├── 📁 data/                           # Data storage directory
├── 📁 templates/                      # Web dashboard templates
├── 📁 static/                         # Static web assets
├── 📁 tests/                          # Test files directory
├── 📁 docs/                           # Documentation directory
├── 📄 linkedin_automation.py          # Core automation engine
├── 📄 enhanced_linkedin_automation.py # Enhanced automation with AI
├── 📄 ai_job_matcher.py              # AI job matching system
├── 📄 database.py                     # Database management
├── 📄 simple_scheduler.py             # Scheduling system
├── 📄 web_dashboard.py                # Web dashboard
├── 📄 main.py                         # Original MVP main application
├── 📄 simple_enhanced_main.py         # Enhanced main application
├── 📄 automated_runner.py             # Non-interactive automation
├── 📄 non_interactive_automation.py   # Pre-configured automation
├── 📄 config.py                       # Configuration management
├── 📄 scheduler_config.json           # Scheduler settings
├── 📄 ai_config.json                  # AI matching settings
├── 📄 dashboard_config.json           # Dashboard settings
├── 📄 config.json                     # User configuration
├── 📄 requirements.txt                # Basic dependencies
├── 📄 requirements_full.txt           # Full dependencies
└── 📄 README.md                       # This file
```

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- Chrome browser installed
- LinkedIn account

### Quick Setup
```bash
# 1. Clone the repository
git clone <repository-url>
cd linkedin-automation

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the automation
python main.py
```

### Full Setup (Enhanced Features)
```bash
# 1. Install full dependencies
pip install -r requirements_full.txt

# 2. Run setup script
python setup_full_project.py

# 3. Configure your settings
cp env_template.txt .env
# Edit .env with your LinkedIn credentials

# 4. Run enhanced automation
python simple_enhanced_main.py
```

## 🚀 Usage

### Quick Start (MVP Version)
```bash
python main.py
```
Interactive setup with basic features.

### Enhanced Version (Recommended)
```bash
python simple_enhanced_main.py
```
Full-featured automation with AI matching and database tracking.

### Non-Interactive Mode
```bash
# 1. Edit config.json with your settings
# 2. Run automation
python automated_runner.py
```

### Web Dashboard
```bash
python web_dashboard.py
# Open http://127.0.0.1:5000 in your browser
```

## ⚙️ Configuration

### Basic Configuration
Edit `config.json`:
```json
{
  "linkedin_email": "your-email@example.com",
  "linkedin_password": "your-password",
  "job_keywords": ["Data Analyst", "Business Analyst"],
  "preferred_location": "San Francisco, CA",
  "max_applications_per_day": 10,
  "experience_years": 3,
  "skills": ["Python", "SQL", "Tableau"],
  "education": ["Bachelor's Degree"],
  "easy_apply_only": true,
  "remote_preference": true,
  "experience_level": "mid",
  "company_size": "medium"
}
```

### Scheduler Configuration
Edit `scheduler_config.json`:
```json
{
  "enabled": true,
  "daily_application_limit": 10,
  "optimal_times": {
    "all_day": {
      "start": "00:00",
      "end": "23:59"
    }
  },
  "weekdays_only": false,
  "auto_pause_on_limit": true
}
```

### AI Configuration
Edit `ai_config.json`:
```json
{
  "min_match_score": 70.0,
  "enable_resume_optimization": true,
  "enable_cover_letter_generation": true,
  "skill_weight": 0.4,
  "experience_weight": 0.25,
  "education_weight": 0.15
}
```

## 📊 Features Comparison

| Feature | MVP Version | Enhanced Version |
|---------|-------------|------------------|
| Job Search | Basic search | AI-powered smart search |
| Data Storage | Log files only | Full database with analytics |
| User Interface | Command line only | Web dashboard + CLI |
| Scheduling | Manual execution | Automated optimal timing |
| Job Matching | No filtering | AI-powered matching |
| Analytics | Basic logging | Comprehensive analytics |
| Multi-account | Single account | Multiple account support |
| Error Handling | Basic | Advanced with recovery |

## 🧪 Testing

### Run Tests
```bash
# Run all tests
pytest tests/ -v

# Run specific test suites
pytest tests/test_linkedin_automation.py -v
pytest tests/test_database.py -v
pytest tests/test_ai_matcher.py -v
```

### Test Coverage
```bash
pytest tests/ --cov=. --cov-report=html
```

## 📈 Usage Examples

### Basic Automation
```python
from linkedin_automation import LinkedInAutomation
from config import LinkedInConfig, JobApplicationConfig

# Setup
linkedin_config = LinkedInConfig(email="user@example.com", password="password")
job_config = JobApplicationConfig(keywords=["Data Analyst"], max_applications_per_day=10)

# Run automation
automation = LinkedInAutomation(linkedin_config, job_config)
result = automation.run_automation()
```

### Enhanced Automation with AI
```python
from enhanced_linkedin_automation import EnhancedLinkedInAutomation

# Enhanced automation with AI matching
automation = EnhancedLinkedInAutomation(linkedin_config, job_config)
result = automation.run_automation_enhanced()
```

### Database Analytics
```python
from database import DatabaseManager

# Get analytics
db_manager = DatabaseManager()
analytics = db_manager.get_analytics(30)
print(f"Total applications: {analytics['total_applications']}")
print(f"Success rate: {analytics['success_rate']}%")
```

### Web Dashboard
```python
from web_dashboard import WebDashboard

# Start dashboard
dashboard = WebDashboard(host='0.0.0.0', port=5000)
dashboard.run()
```

## 🔧 Troubleshooting

### Common Issues

#### Browser Issues
```bash
# Clean up browser processes
python chrome_cleanup.py

# Update ChromeDriver
pip install --upgrade webdriver-manager
```

#### Database Issues
```bash
# Reset database
rm linkedin_automation.db
python main.py  # Will recreate database
```

#### Scheduler Issues
```bash
# Check scheduler status
python -c "from simple_scheduler import SimpleScheduler; s = SimpleScheduler(); print(s.can_apply_now())"
```

#### Configuration Issues
```bash
# Validate configuration
python -c "from config import LinkedInConfig, JobApplicationConfig; print('Config valid')"
```

### Log Files
- `linkedin_automation.log` - Technical logs
- `automation_actions.log` - Action logs
- `enhanced_automation.log` - Enhanced system logs
- `enhanced_actions.log` - Enhanced action logs

### Log Analysis
```bash
# View recent logs
python log_viewer.py

# Clean old logs
python log_cleanup.py
```

## 📚 Documentation

- **[README_MVP.md](README_MVP.md)** - MVP documentation
- **[README_FULL_PROJECT.md](README_FULL_PROJECT.md)** - Full project documentation
- **[QUICK_START.md](QUICK_START.md)** - Quick start guide
- **[FAILURE_FIXES_SUMMARY.md](FAILURE_FIXES_SUMMARY.md)** - Troubleshooting guide
- **[FULL_PROJECT_SUMMARY.md](FULL_PROJECT_SUMMARY.md)** - Project evolution summary

## 🚨 Important Notes

### Legal and Ethical Use
- This tool is for educational and personal use only
- Users are responsible for complying with LinkedIn's Terms of Service
- Respect LinkedIn's rate limits and application guidelines
- Use responsibly and ethically

### Rate Limiting
- Default daily limit: 10 applications per day
- Respects LinkedIn's application limits
- Includes cooldown periods between applications
- Automatically pauses when limits are reached

### Privacy and Security
- All data stored locally
- No external data sharing
- Secure credential management
- GDPR-compliant data handling

## 🤝 Contributing

### Development Setup
```bash
# Install development dependencies
pip install -r requirements_full.txt

# Install pre-commit hooks
pre-commit install

# Run tests
pytest tests/ -v
```

### Code Style
```bash
# Format code
black .

# Lint code
flake8 .

# Type checking
mypy .
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Users are responsible for complying with LinkedIn's Terms of Service and applicable laws. The authors are not responsible for any misuse of this tool.

## 🆘 Support

### Documentation
- Check the documentation files in the `docs/` directory
- Review troubleshooting guides
- Check log files for error details

### Issues
- Report issues on GitHub
- Include log files and error messages
- Provide system information (OS, Python version, etc.)

### Community
- Join discussions on GitHub
- Share experiences and tips
- Contribute improvements

---

**LinkedIn Job Application Automation**  
*Automate your job search with AI-powered intelligence*

**Ready to start your automated job search? Run `python main.py` to begin!** 🚀
