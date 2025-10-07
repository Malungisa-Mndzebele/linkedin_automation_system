"""
Chrome Process Cleanup Utility
This tool helps clean up any existing Chrome processes that might interfere with automation
"""
import os
import subprocess
import sys
import time


def kill_chrome_processes():
    """Kill all Chrome processes on Windows"""
    try:
        # Kill Chrome processes
        subprocess.run(['taskkill', '/f', '/im', 'chrome.exe'], 
                      capture_output=True, text=True)
        
        # Kill ChromeDriver processes
        subprocess.run(['taskkill', '/f', '/im', 'chromedriver.exe'], 
                      capture_output=True, text=True)
        
        print("Chrome processes cleaned up successfully!")
        return True
        
    except Exception as e:
        print(f"Error cleaning up Chrome processes: {e}")
        return False


def check_chrome_processes():
    """Check if Chrome processes are running"""
    try:
        # Check for Chrome processes
        result = subprocess.run(['tasklist', '/fi', 'imagename eq chrome.exe'], 
                              capture_output=True, text=True)
        
        chrome_running = 'chrome.exe' in result.stdout
        
        # Check for ChromeDriver processes
        result = subprocess.run(['tasklist', '/fi', 'imagename eq chromedriver.exe'], 
                              capture_output=True, text=True)
        
        chromedriver_running = 'chromedriver.exe' in result.stdout
        
        return chrome_running, chromedriver_running
        
    except Exception as e:
        print(f"Error checking processes: {e}")
        return False, False


def main():
    """Main function for Chrome cleanup"""
    print("Chrome Process Cleanup Utility")
    print("=" * 40)
    
    # Check current processes
    chrome_running, chromedriver_running = check_chrome_processes()
    
    print(f"Chrome processes running: {'Yes' if chrome_running else 'No'}")
    print(f"ChromeDriver processes running: {'Yes' if chromedriver_running else 'No'}")
    print()
    
    if chrome_running or chromedriver_running:
        print("Found running Chrome/ChromeDriver processes.")
        choice = input("Do you want to kill them? (y/n): ").strip().lower()
        
        if choice == 'y':
            if kill_chrome_processes():
                print("Waiting 3 seconds for processes to close...")
                time.sleep(3)
                
                # Check again
                chrome_running, chromedriver_running = check_chrome_processes()
                print(f"Chrome processes running: {'Yes' if chrome_running else 'No'}")
                print(f"ChromeDriver processes running: {'Yes' if chromedriver_running else 'No'}")
                
                if not chrome_running and not chromedriver_running:
                    print("\n✓ All Chrome processes cleaned up successfully!")
                    print("You can now run the LinkedIn automation.")
                else:
                    print("\n⚠ Some processes may still be running. Try running as administrator.")
            else:
                print("Failed to clean up processes. Try running as administrator.")
        else:
            print("Process cleanup cancelled.")
    else:
        print("No Chrome processes found. You should be able to run the automation.")
    
    print("\nTo run the LinkedIn automation:")
    print("  python main.py")


if __name__ == "__main__":
    main()
