"""
Final ChromeDriver Fix Verification
Tests the complete automation with ChromeDriver fix
"""
import os
import sys

def test_automation_with_chromedriver():
    """Test automation class with ChromeDriver fix"""
    print("Testing automation with ChromeDriver fix...")
    
    try:
        from linkedin_automation import LinkedInAutomation
        from config import LinkedInConfig, JobApplicationConfig
        
        config = LinkedInConfig(
            email="test@example.com",
            password="testpassword",
            job_keywords=["Data Analyst"],
            easy_apply_only=True,
            max_applications_per_day=5,
            headless=True
        )
        
        job_config = JobApplicationConfig()
        automation = LinkedInAutomation(config, job_config)
        
        print("SUCCESS: Automation class created successfully")
        
        # Test driver setup (without actually starting browser)
        try:
            driver = automation._setup_driver()
            if driver:
                print("SUCCESS: ChromeDriver setup successful")
                driver.quit()
                return True
            else:
                print("ERROR: ChromeDriver setup failed")
                return False
        except Exception as e:
            print(f"ERROR: ChromeDriver setup failed: {e}")
            return False
        
    except Exception as e:
        print(f"ERROR: Automation test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("ChromeDriver Fix Verification")
    print("=" * 60)
    
    # Check if local ChromeDriver exists
    local_chromedriver = os.path.join(os.getcwd(), "chromedriver", "chromedriver.exe")
    if os.path.exists(local_chromedriver):
        print(f"SUCCESS: Local ChromeDriver found: {local_chromedriver}")
    else:
        print("ERROR: Local ChromeDriver not found")
        return False
    
    # Test automation
    if test_automation_with_chromedriver():
        print("\n" + "=" * 60)
        print("CHROMEDRIVER FIX COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        print("Your LinkedIn automation web application is now fully functional!")
        print("\nTo test:")
        print("1. Restart your web application")
        print("2. Go to http://localhost:5000")
        print("3. Configure your LinkedIn credentials")
        print("4. Click 'Start Automation'")
        print("5. The browser should now start successfully")
        return True
    else:
        print("\nERROR: ChromeDriver fix verification failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
