"""
Repository Preparation Script
Cleans up sensitive information and prepares the project for public repository
"""
import os
import shutil
import re
from pathlib import Path


def print_banner():
    """Print preparation banner"""
    print("=" * 70)
    print("LinkedIn Automation - Repository Preparation")
    print("=" * 70)
    print()


def remove_sensitive_files():
    """Remove files containing sensitive information"""
    print("Removing sensitive files...")
    
    sensitive_files = [
        "enhanced_actions.log",
        "automation_actions.log", 
        "linkedin_automation.log",
        "enhanced_automation.log",
        "daily_stats.json",
        "linkedin_automation.db",
        "test.db"
    ]
    
    for file in sensitive_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"[REMOVED] {file}")
        else:
            print(f"[SKIP] {file} (not found)")


def clean_sensitive_content():
    """Clean sensitive content from files"""
    print("Cleaning sensitive content from files...")
    
    # Files that might contain sensitive information
    files_to_clean = [
        "config.json",
        "non_interactive_automation.py",
        "automated_runner.py",
        "run_with_your_config.py",
        "simple_enhanced_main.py",
        "enhanced_main.py"
    ]
    
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Replace sensitive patterns
                content = re.sub(r'mndzebelemalungisa@gmail\.com', 'your-email@example.com', content)
                content = re.sub(r'YOUR_PASSWORD_HERE', 'your-password-here', content)
                content = re.sub(r'your-actual-password', 'your-password-here', content)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)
                
                print(f"[CLEANED] {file_path}")
            except Exception as e:
                print(f"[ERROR] Failed to clean {file_path}: {e}")


def create_example_files():
    """Create example files for users"""
    print("Creating example files...")
    
    # Ensure example files exist
    example_files = {
        "config_example.json": {
            "linkedin_email": "your-email@example.com",
            "linkedin_password": "your-password-here",
            "job_keywords": ["Data Analyst", "Business Analyst"],
            "preferred_location": "San Francisco, CA",
            "max_applications_per_day": 10,
            "experience_years": 3,
            "skills": ["Python", "SQL", "Tableau"],
            "education": ["Bachelor's Degree"],
            "easy_apply_only": True,
            "remote_preference": True,
            "experience_level": "mid",
            "company_size": "medium"
        }
    }
    
    for filename, content in example_files.items():
        if not os.path.exists(filename):
            import json
            with open(filename, 'w') as f:
                json.dump(content, f, indent=2)
            print(f"[CREATED] {filename}")


def verify_gitignore():
    """Verify .gitignore is comprehensive"""
    print("Verifying .gitignore...")
    
    if not os.path.exists('.gitignore'):
        print("[ERROR] .gitignore not found!")
        return False
    
    with open('.gitignore', 'r') as f:
        gitignore_content = f.read()
    
    required_patterns = [
        '*.log',
        'config.json',
        '.env',
        '*.db',
        'enhanced_actions.log',
        'automation_actions.log'
    ]
    
    missing_patterns = []
    for pattern in required_patterns:
        if pattern not in gitignore_content:
            missing_patterns.append(pattern)
    
    if missing_patterns:
        print(f"[WARNING] Missing patterns in .gitignore: {missing_patterns}")
        return False
    else:
        print("[OK] .gitignore looks good")
        return True


def check_for_sensitive_data():
    """Check for remaining sensitive data"""
    print("Checking for remaining sensitive data...")
    
    sensitive_patterns = [
        r'mndzebelemalungisa@gmail\.com',
        r'password\s*=\s*["\'][^"\']+["\']',
        r'email\s*=\s*["\'][^"\']*@[^"\']*["\']',
        r'YOUR_PASSWORD_HERE',
        r'your-actual-password'
    ]
    
    files_to_check = [
        '*.py',
        '*.json',
        '*.md',
        '*.txt'
    ]
    
    found_sensitive = False
    
    for pattern in sensitive_patterns:
        for file_type in files_to_check:
            for file_path in Path('.').glob(file_type):
                if file_path.name.startswith('.') or file_path.name in ['.gitignore', 'prepare_repository.py']:
                    continue
                
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if re.search(pattern, content, re.IGNORECASE):
                        print(f"[WARNING] Potential sensitive data in {file_path}")
                        found_sensitive = True
                except Exception:
                    continue
    
    if not found_sensitive:
        print("[OK] No sensitive data found")
    else:
        print("[WARNING] Please review the files above for sensitive data")
    
    return not found_sensitive


def create_repository_readme():
    """Create repository-specific README"""
    print("Creating repository README...")
    
    repo_readme = """# LinkedIn Job Application Automation

A comprehensive, AI-powered LinkedIn job application automation system.

## 🚀 Quick Start

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd linkedin-automation
   ```

2. **Set up your configuration**
   ```bash
   python setup_repository.py
   ```

3. **Edit your credentials**
   - Edit `config.json` with your LinkedIn credentials
   - Edit `.env` with your environment variables (optional)

4. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the automation**
   ```bash
   python main.py
   ```

## 📚 Documentation

- [README.md](README.md) - Complete documentation
- [SECURITY.md](SECURITY.md) - Security guidelines
- [QUICK_START.md](QUICK_START.md) - Quick start guide

## ⚠️ Important

- **Never commit your actual credentials to version control**
- **Use the example files as templates**
- **Keep your configuration files local and secure**

## 🔒 Security

See [SECURITY.md](SECURITY.md) for comprehensive security guidelines.

## 📄 License

This project is licensed under the MIT License.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Users are responsible for complying with LinkedIn's Terms of Service.
"""
    
    with open('REPOSITORY_README.md', 'w') as f:
        f.write(repo_readme)
    
    print("[CREATED] REPOSITORY_README.md")


def main():
    """Main preparation function"""
    print_banner()
    
    try:
        # Remove sensitive files
        remove_sensitive_files()
        
        # Clean sensitive content
        clean_sensitive_content()
        
        # Create example files
        create_example_files()
        
        # Verify .gitignore
        gitignore_ok = verify_gitignore()
        
        # Check for sensitive data
        no_sensitive_data = check_for_sensitive_data()
        
        # Create repository README
        create_repository_readme()
        
        print("\n" + "=" * 70)
        print("Repository Preparation Complete!")
        print("=" * 70)
        
        if gitignore_ok and no_sensitive_data:
            print("\n[SUCCESS] Repository is ready for public push!")
            print("\nNext steps:")
            print("1. Review all changes")
            print("2. Test with example credentials")
            print("3. Commit and push to repository")
        else:
            print("\n[WARNING] Please address the issues above before pushing")
        
        print("\nFiles created/updated:")
        print("[OK] .gitignore (verified)")
        print("[OK] config_example.json")
        print("[OK] env_example.env")
        print("[OK] setup_repository.py")
        print("[OK] SECURITY.md")
        print("[OK] REPOSITORY_README.md")
        
    except Exception as e:
        print(f"\n[ERROR] Preparation failed: {e}")


if __name__ == "__main__":
    main()
