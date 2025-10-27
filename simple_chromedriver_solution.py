"""
Simple ChromeDriver Solution
Uses webdriver-manager with fallback options
"""
import os
import sys

def create_simple_test():
    """Create a simple test to verify ChromeDriver works"""
    print("🧪 Creating simple ChromeDriver test...")
    
    test_code = '''
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def test_chromedriver():
    """Test ChromeDriver with multiple fallback options"""
    print("Testing ChromeDriver...")
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--disable-web-security")
    chrome_options.add_argument("--allow-running-insecure-content")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-plugins")
    
    # Try multiple approaches
    approaches = [
        ("webdriver-manager", lambda: Service(ChromeDriverManager().install())),
        ("local chromedriver", lambda: Service(os.path.join(os.getcwd(), "chromedriver", "chromedriver.exe"))),
        ("no service", lambda: None)
    ]
    
    for approach_name, service_func in approaches:
        try:
            print(f"Trying {approach_name}...")
            service = service_func()
            
            if service is None:
                driver = webdriver.Chrome(options=chrome_options)
            else:
                driver = webdriver.Chrome(service=service, options=chrome_options)
            
            # Test basic functionality
            driver.get("https://www.google.com")
            title = driver.title
            driver.quit()
            
            print(f"✅ {approach_name} successful! Page title: {title}")
            return True
            
        except Exception as e:
            print(f"❌ {approach_name} failed: {e}")
            continue
    
    print("❌ All approaches failed")
    return False

if __name__ == "__main__":
    success = test_chromedriver()
    sys.exit(0 if success else 1)
'''
    
    with open('simple_chromedriver_test.py', 'w') as f:
        f.write(test_code)
    
    print("✅ Simple test created")
    return True

def run_simple_test():
    """Run the simple ChromeDriver test"""
    print("🧪 Running simple ChromeDriver test...")
    
    try:
        import subprocess
        result = subprocess.run([sys.executable, 'simple_chromedriver_test.py'], 
                              capture_output=True, text=True, timeout=60)
        
        print("Test output:")
        print(result.stdout)
        if result.stderr:
            print("Test errors:")
            print(result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ Test execution failed: {e}")
        return False

def update_automation_with_fallback():
    """Update automation code with better fallback handling"""
    print("🔧 Updating automation code with fallback handling...")
    
    try:
        # Read current file
        with open('linkedin_automation.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add better error handling
        new_driver_code = '''
        # Use webdriver-manager to automatically handle ChromeDriver
        service = None
        driver = None
        
        # Try multiple approaches for ChromeDriver
        approaches = [
            ("webdriver-manager", lambda: Service(ChromeDriverManager().install())),
            ("local chromedriver", lambda: Service(os.path.join(os.getcwd(), "chromedriver", "chromedriver.exe")) if os.path.exists(os.path.join(os.getcwd(), "chromedriver", "chromedriver.exe")) else None),
            ("no service", lambda: None)
        ]
        
        for approach_name, service_func in approaches:
            try:
                self.logger.info(f"Trying ChromeDriver approach: {approach_name}")
                service = service_func()
                
                if service is None:
                    driver = webdriver.Chrome(options=chrome_options)
                else:
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                
                self.logger.info(f"✅ ChromeDriver {approach_name} successful")
                break
                
            except Exception as e:
                self.logger.warning(f"ChromeDriver {approach_name} failed: {e}")
                if driver:
                    try:
                        driver.quit()
                    except:
                        pass
                driver = None
                continue
        
        if driver is None:
            raise Exception("All ChromeDriver approaches failed")
        '''
        
        # Find and replace the driver creation code
        old_code_start = "        # Use webdriver-manager to automatically handle ChromeDriver"
        old_code_end = "        driver = webdriver.Chrome(service=service, options=chrome_options)"
        
        if old_code_start in content and old_code_end in content:
            start_idx = content.find(old_code_start)
            end_idx = content.find(old_code_end) + len(old_code_end)
            
            new_content = content[:start_idx] + new_driver_code + content[end_idx:]
            
            with open('linkedin_automation.py', 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print("✅ Automation code updated with fallback handling")
            return True
        else:
            print("⚠️ Could not find exact code to replace")
            return False
            
    except Exception as e:
        print(f"❌ Error updating automation code: {e}")
        return False

def main():
    """Main function"""
    print("=" * 60)
    print("Simple ChromeDriver Solution")
    print("=" * 60)
    
    # Create simple test
    if not create_simple_test():
        print("❌ Failed to create test")
        return False
    
    # Run test
    if run_simple_test():
        print("\n🎉 ChromeDriver is working!")
        
        # Update automation code
        if update_automation_with_fallback():
            print("✅ Automation code updated with fallback handling")
        
        print("\n🚀 Your automation should now work!")
        print("To test:")
        print("1. Restart your web application")
        print("2. Go to dashboard")
        print("3. Click 'Start Automation'")
        
        return True
    else:
        print("\n❌ ChromeDriver test failed")
        print("📝 Manual steps:")
        print("1. Update Chrome to a stable version")
        print("2. Or download ChromeDriver manually")
        print("3. Place chromedriver.exe in the chromedriver folder")
        
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
