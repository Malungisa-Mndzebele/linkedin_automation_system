"""
Setup script for LinkedIn Job Application Automation MVP
This script helps you set up the required environment variables
"""
import os
import sys


def setup_environment():
    """Setup environment variables for the LinkedIn automation"""
    print("=" * 60)
    print("LinkedIn Job Application Automation MVP - Setup")
    print("=" * 60)
    
    # Get credentials from user
    print("\nPlease enter your LinkedIn credentials:")
    email = input("LinkedIn Email: ").strip()
    password = input("LinkedIn Password: ").strip()
    
    if not email or not password:
        print("\n[ERROR] Email and password are required!")
        return False
    
    # Set environment variables for current session
    os.environ['LINKEDIN_EMAIL'] = email
    os.environ['LINKEDIN_PASSWORD'] = password
    os.environ['JOB_KEYWORDS'] = 'Data Analyst,Business Analyst,Data Scientist'
    os.environ['EASY_APPLY_ONLY'] = 'true'
    os.environ['MAX_APPLICATIONS_PER_DAY'] = '10'
    os.environ['HEADLESS'] = 'false'
    os.environ['IMPLICIT_WAIT'] = '10'
    os.environ['PAGE_LOAD_TIMEOUT'] = '30'
    
    print("\n[SUCCESS] Environment variables set for current session!")
    print("\nConfiguration:")
    print(f"  Email: {email}")
    print(f"  Job Keywords: Data Analyst, Business Analyst, Data Scientist")
    print(f"  Easy Apply Only: true")
    print(f"  Max Applications/Day: 10")
    print(f"  Headless Mode: false")
    
    return True


def create_batch_file():
    """Create a Windows batch file to set environment variables permanently"""
    batch_content = """@echo off
REM LinkedIn Job Application Automation MVP - Environment Setup
REM Run this file to set environment variables for the current session

echo Setting up LinkedIn automation environment variables...

REM Set LinkedIn credentials (replace with your actual credentials)
set LINKEDIN_EMAIL=your-email@example.com
set LINKEDIN_PASSWORD=your-password-here

REM Set job search settings
set JOB_KEYWORDS=Data Analyst,Business Analyst,Data Scientist
set EASY_APPLY_ONLY=true
set MAX_APPLICATIONS_PER_DAY=10

REM Set browser settings
set HEADLESS=false
set IMPLICIT_WAIT=10
set PAGE_LOAD_TIMEOUT=30

echo Environment variables set successfully!
echo You can now run: python main.py
pause
"""
    
    with open('setup_env.bat', 'w') as f:
        f.write(batch_content)
    
    print("\n[INFO] Created 'setup_env.bat' file for Windows environment setup")
    print("You can run this batch file to set environment variables permanently")


def main():
    """Main setup function"""
    print("Choose setup method:")
    print("1. Set environment variables for current session only")
    print("2. Create Windows batch file for permanent setup")
    print("3. Both")
    
    choice = input("\nEnter your choice (1-3): ").strip()
    
    if choice in ['1', '3']:
        if setup_environment():
            print("\n" + "=" * 60)
            print("You can now run the automation:")
            print("  python main.py")
            print("=" * 60)
    
    if choice in ['2', '3']:
        create_batch_file()
    
    if choice not in ['1', '2', '3']:
        print("\n[ERROR] Invalid choice. Please run the script again.")


if __name__ == "__main__":
    main()
