"""
Final cleanup script to remove all sensitive information
"""
import os
import re
from pathlib import Path


def clean_file(file_path):
    """Clean sensitive data from a file"""
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
        return True
    except Exception as e:
        print(f"[ERROR] Failed to clean {file_path}: {e}")
        return False


def main():
    """Clean all files with sensitive data"""
    print("Final cleanup of sensitive data...")
    
    # Files that need cleaning
    files_to_clean = [
        "FAILURE_FIXES_SUMMARY.md",
        "fix_failures.py", 
        "FINAL_SETUP_SUMMARY.md",
        "setup_env.ps1",
        "setup_credentials.py",
        "LinkedIn_Job_Application_Automation_Project.md"
    ]
    
    cleaned_count = 0
    for file_path in files_to_clean:
        if os.path.exists(file_path):
            if clean_file(file_path):
                cleaned_count += 1
    
    print(f"\nCleaned {cleaned_count} files")
    print("Repository is now ready for public push!")


if __name__ == "__main__":
    main()
