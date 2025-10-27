"""
Quick ChromeDriver Test
Tests if the ChromeDriver fix is working
"""
import os
import sys

def test_chromedriver_fix():
    """Test if ChromeDriver fix is working"""
    print("🧪 Testing ChromeDriver fix...")
    
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        
        # Check if local ChromeDriver exists
        local_chromedriver = os.path.join(os.getcwd(), "chromedriver", "chromedriver.exe")
        if not os.path.exists(local_chromedriver):
            print("❌ Local ChromeDriver not found")
            return False
        
        print(f"✅ Local ChromeDriver found: {local_chromedriver}")
        
        # Test ChromeDriver
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        service = Service(local_chromedriver)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Test basic functionality
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ ChromeDriver test successful! Page title: {title}")
        return True
        
    except Exception as e:
        print(f"❌ ChromeDriver test failed: {e}")
        return False

def test_automation_class():
    """Test if automation class works with ChromeDriver fix"""
    print("🧪 Testing automation class...")
    
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
        
        # Test driver setup (without actually starting browser)
        print("✅ Automation class created successfully")
        
        # Test statistics
        stats = automation.get_application_stats()
        print(f"✅ Application stats: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Automation class test failed: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("ChromeDriver Fix Verification")
    print("=" * 60)
    
    # Test ChromeDriver
    chromedriver_ok = test_chromedriver_fix()
    
    # Test automation class
    automation_ok = test_automation_class()
    
    print("\n" + "=" * 60)
    print("TEST RESULTS")
    print("=" * 60)
    
    if chromedriver_ok and automation_ok:
        print("🎉 ChromeDriver fix completed successfully!")
        print("✅ Your automation should now work properly")
        print("\n🚀 To test the full automation:")
        print("   1. Restart your web application")
        print("   2. Go to the dashboard")
        print("   3. Click 'Start Automation'")
        print("   4. The browser should now start successfully")
        return True
    else:
        print("❌ Some tests failed")
        if not chromedriver_ok:
            print("   - ChromeDriver test failed")
        if not automation_ok:
            print("   - Automation class test failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
