"""
Log Cleanup Utility for LinkedIn Job Application Automation
This tool helps manage and clean up log files
"""
import os
import shutil
from datetime import datetime, timedelta


def backup_logs():
    """Create a backup of current log files"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_dir = f"log_backup_{timestamp}"
    
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    
    log_files = ['linkedin_automation.log', 'automation_actions.log']
    backed_up_files = []
    
    for log_file in log_files:
        if os.path.exists(log_file):
            backup_path = os.path.join(backup_dir, log_file)
            shutil.copy2(log_file, backup_path)
            backed_up_files.append(log_file)
    
    if backed_up_files:
        print(f"Backup created in '{backup_dir}' with files:")
        for file in backed_up_files:
            print(f"  - {file}")
    else:
        print("No log files found to backup.")
        os.rmdir(backup_dir)
    
    return len(backed_up_files) > 0


def clear_logs():
    """Clear all log files"""
    log_files = ['linkedin_automation.log', 'automation_actions.log']
    cleared_files = []
    
    for log_file in log_files:
        if os.path.exists(log_file):
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write(f"Log file cleared on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            cleared_files.append(log_file)
    
    if cleared_files:
        print("Cleared log files:")
        for file in cleared_files:
            print(f"  - {file}")
    else:
        print("No log files found to clear.")


def get_log_sizes():
    """Get the size of log files"""
    log_files = ['linkedin_automation.log', 'automation_actions.log']
    total_size = 0
    
    print("Log file sizes:")
    for log_file in log_files:
        if os.path.exists(log_file):
            size = os.path.getsize(log_file)
            total_size += size
            size_mb = size / (1024 * 1024)
            print(f"  - {log_file}: {size_mb:.2f} MB")
        else:
            print(f"  - {log_file}: Not found")
    
    print(f"Total size: {total_size / (1024 * 1024):.2f} MB")


def main():
    """Main function for log cleanup utility"""
    print("LinkedIn Job Application Automation - Log Cleanup Utility")
    print("=" * 60)
    print("1. View log file sizes")
    print("2. Backup log files")
    print("3. Clear log files")
    print("4. Exit")
    print()
    
    while True:
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            get_log_sizes()
        elif choice == '2':
            if backup_logs():
                print("Backup completed successfully!")
            else:
                print("No files to backup.")
        elif choice == '3':
            confirm = input("Are you sure you want to clear all log files? (y/n): ").strip().lower()
            if confirm == 'y':
                clear_logs()
                print("Log files cleared.")
            else:
                print("Operation cancelled.")
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please select 1-4.")
        
        print("\n" + "-" * 60)


if __name__ == "__main__":
    main()
