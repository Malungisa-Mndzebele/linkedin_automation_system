"""
Test script to verify Chrome driver fix
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from linkedin_automation import LinkedInAutomation
from config import LinkedInConfig, JobApplicationConfig


def test_chrome_driver():
    """Test Chrome driver setup with unique user data directory"""
    print("Testing Chrome driver setup...")
    
    # Create test configuration
    config = LinkedInConfig(
        email="test@example.com",
        password="testpassword",
        headless=False,
        implicit_wait=5,
        page_load_timeout=10
    )
    job_config = JobApplicationConfig()
    
    # Initialize automation
    automation = LinkedInAutomation(config, job_config)
    
    try:
        # Test driver setup
        print("Setting up Chrome driver...")
        driver = automation._setup_driver()
        print("[SUCCESS] Chrome driver setup successful!")
        
        # Test basic navigation
        print("Testing basic navigation...")
        driver.get("https://www.google.com")
        print("[SUCCESS] Navigation test successful!")
        
        # Close driver
        driver.quit()
        print("[SUCCESS] Driver cleanup successful!")
        
        print("\n*** Chrome driver fix is working correctly! ***")
        return True
        
    except Exception as e:
        print(f"[FAILED] Chrome driver test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_chrome_driver()
    sys.exit(0 if success else 1)
