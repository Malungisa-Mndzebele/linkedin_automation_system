# LinkedIn Job Application Automation MVP

A Python-based automation tool for LinkedIn job searching and application using Selenium WebDriver.

## 🚀 Features

- **Automated LinkedIn Login**: Secure authentication with credential management
- **Smart Job Search**: Search for specific roles with customizable keywords
- **Easy Apply Automation**: Automatically apply to jobs with one-click application
- **Application Tracking**: Monitor daily application limits and statistics
- **Messaging Integration**: Send automated messages to recruiters
- **Comprehensive Testing**: Full unit and integration test coverage

## 📋 Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- LinkedIn account with valid credentials
- ChromeDriver (automatically managed by webdriver-manager)

## 🛠️ Installation

1. **Clone or download the project files**

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**:
   ```bash
   # Copy the example environment file
   cp env_example.txt .env
   
   # Edit .env with your credentials
   LINKEDIN_EMAIL=your_email@example.com
   LINKEDIN_PASSWORD=your_password
   JOB_KEYWORDS=Data Analyst,Business Analyst
   EASY_APPLY_ONLY=true
   MAX_APPLICATIONS_PER_DAY=10
   ```

## 🏃‍♂️ Quick Start

### Basic Usage

```python
from linkedin_automation import LinkedInAutomation
from config import LinkedInConfig, JobApplicationConfig

# Load configuration
config = LinkedInConfig.from_env()
job_config = JobApplicationConfig()

# Initialize automation
automation = LinkedInAutomation(config, job_config)

# Start session and login
automation.start_session()
automation.login()

# Search for jobs
automation.search_jobs()

# Get and apply to jobs
jobs = automation.get_job_listings(max_jobs=5)
for job in jobs:
    if job['has_easy_apply']:
        automation.apply_to_job(job)

# Close session
automation.close_session()
```

### Using the Main Script

```bash
python main.py
```

## 🧪 Testing

### Run All Tests
```bash
pytest
```

### Run Specific Test Types
```bash
# Unit tests only
pytest -m unit

# Integration tests only
pytest -m integration

# Run with verbose output
pytest -v
```

### Test Coverage
```bash
# Install coverage (if not already installed)
pip install pytest-cov

# Run tests with coverage
pytest --cov=. --cov-report=html
```

## 📁 Project Structure

```
linkedin-mvp/
├── config.py                 # Configuration management
├── linkedin_automation.py    # Core automation class
├── main.py                   # Main entry point
├── requirements.txt          # Python dependencies
├── pytest.ini              # Test configuration
├── env_example.txt         # Environment variables template
├── test_config.py          # Configuration tests
├── test_linkedin_automation.py  # Automation class tests
├── test_integration.py     # Integration tests
└── README_MVP.md          # This file
```

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `LINKEDIN_EMAIL` | Your LinkedIn email | Required |
| `LINKEDIN_PASSWORD` | Your LinkedIn password | Required |
| `JOB_KEYWORDS` | Comma-separated job keywords | "Data Analyst" |
| `EASY_APPLY_ONLY` | Only apply to Easy Apply jobs | true |
| `MAX_APPLICATIONS_PER_DAY` | Daily application limit | 10 |
| `HEADLESS` | Run browser in headless mode | false |
| `IMPLICIT_WAIT` | Wait time for elements (seconds) | 10 |
| `PAGE_LOAD_TIMEOUT` | Page load timeout (seconds) | 30 |

### Customizing Job Search

```python
# Custom job keywords
config = LinkedInConfig(
    email="your@email.com",
    password="your_password",
    job_keywords=["Data Scientist", "ML Engineer", "AI Researcher"],
    easy_apply_only=True,
    max_applications_per_day=15
)

# Custom job application settings
job_config = JobApplicationConfig(
    auto_apply=True,
    send_messages=True,
    message_template="Hello, I'm very interested in this position!",
    preferred_companies=["Google", "Microsoft", "Amazon"],
    min_salary=80000
)
```

## 🔧 API Reference

### LinkedInAutomation Class

#### Methods

- `start_session()`: Initialize browser session
- `login()`: Login to LinkedIn
- `search_jobs(keywords=None)`: Search for jobs
- `get_job_listings(max_jobs=10)`: Get available job listings
- `apply_to_job(job_info)`: Apply to a specific job
- `send_message(message, recipient_url=None)`: Send LinkedIn message
- `close_session()`: Close browser session
- `get_application_stats()`: Get application statistics

#### Example Usage

```python
# Initialize automation
automation = LinkedInAutomation(config, job_config)

# Complete workflow
automation.start_session()
automation.login()
automation.search_jobs(["Data Analyst", "Business Analyst"])

jobs = automation.get_job_listings(max_jobs=5)
for job in jobs:
    print(f"Found: {job['title']} at {job['company']}")
    if job['has_easy_apply']:
        automation.apply_to_job(job)

stats = automation.get_application_stats()
print(f"Applications sent: {stats['applications_today']}")

automation.close_session()
```

## 🛡️ Security & Best Practices

### Credential Management
- Store credentials in environment variables, never in code
- Use `.env` files for local development
- Consider using a secrets management service for production

### LinkedIn Compliance
- Respect LinkedIn's rate limits
- Use realistic delays between actions
- Monitor for any policy changes
- Keep automation behavior human-like

### Error Handling
- The system includes comprehensive error handling
- Failed operations are logged with detailed information
- Graceful degradation when elements are not found

## 🐛 Troubleshooting

### Common Issues

1. **ChromeDriver Issues**
   ```bash
   # Update Chrome browser
   # The webdriver-manager will automatically handle ChromeDriver
   ```

2. **Login Failures**
   - Verify credentials are correct
   - Check if LinkedIn requires additional verification
   - Ensure account is not locked

3. **Element Not Found Errors**
   - LinkedIn may have changed their page structure
   - Check if you're being rate-limited
   - Verify internet connection

4. **Application Failures**
   - Some jobs may require additional information
   - Check if Easy Apply is actually available
   - Verify daily application limits

### Debug Mode

Enable debug logging:
```python
import logging
logging.getLogger().setLevel(logging.DEBUG)
```

## 📊 Monitoring & Analytics

### Application Statistics
```python
stats = automation.get_application_stats()
print(f"Applications today: {stats['applications_today']}")
print(f"Remaining applications: {stats['remaining_applications']}")
```

### Logging
- All operations are logged to console and `linkedin_automation.log`
- Log levels: INFO, WARNING, ERROR
- Timestamps included for all log entries

## 🚀 Future Enhancements

- [ ] AI-powered job matching
- [ ] Resume optimization
- [ ] Interview scheduling
- [ ] Advanced filtering options
- [ ] Multi-account support
- [ ] Web dashboard
- [ ] Email notifications

## 📄 License

This project is for educational and personal use only. Please respect LinkedIn's Terms of Service and use responsibly.

## ⚠️ Disclaimer

This tool is provided as-is for educational purposes. Users are responsible for:
- Complying with LinkedIn's Terms of Service
- Using the tool ethically and responsibly
- Managing their own application strategy
- Respecting rate limits and platform policies

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📞 Support

For issues and questions:
1. Check the troubleshooting section
2. Review the test cases for usage examples
3. Check the logs for detailed error information
4. Ensure all dependencies are properly installed
