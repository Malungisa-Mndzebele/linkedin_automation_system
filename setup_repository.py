"""
Setup script for LinkedIn Job Application Automation Repository
Helps users set up the project securely without exposing sensitive information
"""
import os
import json
import shutil
from pathlib import Path


def print_banner():
    """Print setup banner"""
    print("=" * 70)
    print("LinkedIn Job Application Automation - Repository Setup")
    print("=" * 70)
    print()


def create_user_config():
    """Create user configuration file"""
    print("Creating user configuration...")
    
    # Check if config.json already exists
    if os.path.exists('config.json'):
        print("[INFO] config.json already exists")
        return
    
    # Copy example config
    if os.path.exists('config_example.json'):
        shutil.copy('config_example.json', 'config.json')
        print("[OK] Created config.json from example")
    else:
        # Create default config
        default_config = {
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
        
        with open('config.json', 'w') as f:
            json.dump(default_config, f, indent=2)
        
        print("[OK] Created default config.json")


def create_env_file():
    """Create environment file"""
    print("Creating environment file...")
    
    # Check if .env already exists
    if os.path.exists('.env'):
        print("[INFO] .env already exists")
        return
    
    # Copy example env
    if os.path.exists('env_example.env'):
        shutil.copy('env_example.env', '.env')
        print("[OK] Created .env from example")
    else:
        print("[WARNING] env_example.env not found")


def create_directories():
    """Create necessary directories"""
    print("Creating project directories...")
    
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


def create_gitignore():
    """Ensure .gitignore exists"""
    print("Checking .gitignore...")
    
    if os.path.exists('.gitignore'):
        print("[OK] .gitignore already exists")
    else:
        print("[WARNING] .gitignore not found - please create one")


def print_setup_instructions():
    """Print setup instructions"""
    print("\n" + "=" * 70)
    print("Setup Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Edit config.json with your LinkedIn credentials and preferences")
    print("2. Edit .env with your environment variables (optional)")
    print("3. Install dependencies: pip install -r requirements.txt")
    print("4. Run the automation: python main.py")
    print()
    print("Important:")
    print("- Never commit your actual credentials to version control")
    print("- Keep config.json and .env files local and secure")
    print("- Use the example files as templates")
    print()
    print("Files created:")
    print("[OK] config.json (edit with your credentials)")
    print("[OK] .env (edit with your environment variables)")
    print("[OK] Project directories")
    print()
    print("For more information, see README.md")


def main():
    """Main setup function"""
    print_banner()
    
    try:
        create_user_config()
        create_env_file()
        create_directories()
        create_gitignore()
        print_setup_instructions()
        
    except Exception as e:
        print(f"[ERROR] Setup failed: {e}")
        print("Please check the error and try again")


if __name__ == "__main__":
    main()
