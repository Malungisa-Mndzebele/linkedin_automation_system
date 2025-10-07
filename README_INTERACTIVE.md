# LinkedIn Job Application Automation - Interactive Version

## 🚀 Quick Start

The main script now prompts you for all required information, making it easy to use without setting up environment variables.

### Running the Automation

```bash
python main.py
```

### What You'll Be Prompted For:

1. **LinkedIn Credentials**
   - Email address
   - Password (hidden input for security)

2. **Job Search Configuration**
   - Job keywords (comma-separated)
   - Example: `Data Analyst, Business Analyst, Data Scientist`

3. **Application Settings**
   - Maximum applications per day (default: 10)
   - Easy Apply only option (default: Yes)

4. **Confirmation**
   - Review your settings before proceeding

### Example Session

```
============================================================
LinkedIn Job Application Automation MVP
============================================================
This tool will help you automatically search and apply for jobs on LinkedIn.
You'll be prompted for your credentials and job search preferences.

Please enter your LinkedIn credentials:
LinkedIn Email: your.email@example.com
LinkedIn Password: [hidden]

Job Search Configuration:
Enter job keywords (comma-separated, e.g., 'Data Analyst, Business Analyst'):
Job Keywords: Data Analyst, Business Analyst

Application Settings:
Maximum applications per day (default: 10): 15
Only apply to Easy Apply jobs? (y/n, default: y): y

============================================================
Configuration Summary:
============================================================
Email: your.email@example.com
Job Keywords: Data Analyst, Business Analyst
Max Applications/Day: 15
Easy Apply Only: Yes
============================================================

Proceed with these settings? (y/n): y
```

### Demo Mode

To see the input flow without running the actual automation:

```bash
python demo_interactive.py
```

## 🔧 Features

- **Interactive Setup**: No need to configure environment variables
- **Secure Password Input**: Password is hidden during input
- **Flexible Job Search**: Enter multiple keywords separated by commas
- **Customizable Limits**: Set your own daily application limits
- **Confirmation Step**: Review settings before proceeding
- **Clear Feedback**: Detailed progress and results display

## 🛡️ Security

- Passwords are entered securely (hidden input)
- No credentials are stored in files
- All sensitive data is handled in memory only
- Detailed logging for troubleshooting

## 📊 Output

The automation provides:
- Real-time progress updates
- Application statistics
- Detailed logging to `linkedin_automation.log`
- Clear success/error messages

## 🎯 Example Use Cases

### Data Analyst Job Search
```
Job Keywords: Data Analyst, Business Analyst, Data Scientist
Max Applications: 10
Easy Apply Only: Yes
```

### Software Developer Search
```
Job Keywords: Software Developer, Python Developer, Full Stack Developer
Max Applications: 15
Easy Apply Only: Yes
```

### Marketing Roles
```
Job Keywords: Marketing Manager, Digital Marketing, Content Marketing
Max Applications: 8
Easy Apply Only: No
```

## 🚨 Important Notes

- **LinkedIn Verification**: You may need to complete additional verification steps
- **Rate Limiting**: The tool respects LinkedIn's rate limits
- **Browser Visibility**: Browser runs in visible mode for user interaction
- **Manual Intervention**: Some steps may require manual confirmation

## 🔍 Troubleshooting

### Common Issues

1. **Login Verification Required**
   - LinkedIn may require additional verification
   - Complete the verification manually in the browser
   - The automation will continue after verification

2. **No Jobs Found**
   - Try different keywords
   - Check if Easy Apply filter is too restrictive
   - Verify your location settings

3. **Application Failures**
   - Some jobs may require additional information
   - Check the log file for detailed error messages
   - Ensure your LinkedIn profile is complete

### Log Files

Check `linkedin_automation.log` for detailed information about:
- Login attempts
- Job search results
- Application status
- Error messages

## 🎉 Success!

When the automation completes successfully, you'll see:

```
============================================================
FINAL RESULTS
============================================================
Applications sent today: 5
Remaining applications: 5
============================================================

*** LinkedIn automation completed successfully! ***
Check the 'linkedin_automation.log' file for detailed logs.
```
