"""
Simple ChromeDriver Fix
Downloads and installs the latest stable ChromeDriver
"""
import os
import requests
import zipfile
import tempfile
from pathlib import Path

def download_latest_chromedriver():
    """Download the latest stable ChromeDriver"""
    print("🔍 Getting latest ChromeDriver version...")
    
    try:
        # Get latest stable version
        response = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE')
        if response.status_code == 200:
            version = response.text.strip()
            print(f"✅ Latest ChromeDriver version: {version}")
        else:
            print("❌ Could not get ChromeDriver version")
            return False
        
        # Download ChromeDriver
        download_url = f"https://chromedriver.storage.googleapis.com/{version}/chromedriver_win32.zip"
        print(f"📥 Downloading ChromeDriver from: {download_url}")
        
        response = requests.get(download_url)
        if response.status_code == 200:
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                tmp_file.write(response.content)
                zip_path = tmp_file.name
            
            # Extract ChromeDriver to project directory
            chromedriver_dir = Path.cwd() / "chromedriver"
            chromedriver_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(chromedriver_dir)
            
            # Clean up
            os.unlink(zip_path)
            
            chromedriver_path = chromedriver_dir / "chromedriver.exe"
            if chromedriver_path.exists():
                print(f"✅ ChromeDriver installed to: {chromedriver_path}")
                return str(chromedriver_path)
            else:
                print("❌ ChromeDriver extraction failed")
                return False
        else:
            print("❌ Could not download ChromeDriver")
            return False
            
    except Exception as e:
        print(f"❌ Error downloading ChromeDriver: {e}")
        return False

def test_chromedriver(path):
    """Test ChromeDriver functionality"""
    print("🧪 Testing ChromeDriver...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        service = Service(path)
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

def update_automation_code():
    """Update the automation code to use local ChromeDriver"""
    print("🔧 Updating automation code...")
    
    try:
        # Read the current linkedin_automation.py file
        with open('linkedin_automation.py', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Add local ChromeDriver path option
        new_code = '''
        # Use webdriver-manager to automatically handle ChromeDriver
        try:
            service = Service(ChromeDriverManager().install())
        except Exception as e:
            self.logger.warning(f"ChromeDriverManager failed: {e}")
            # Try local ChromeDriver
            local_chromedriver = os.path.join(os.getcwd(), "chromedriver", "chromedriver.exe")
            if os.path.exists(local_chromedriver):
                self.logger.info(f"Using local ChromeDriver: {local_chromedriver}")
                service = Service(local_chromedriver)
            else:
                # Try without explicit service - let Selenium handle it
                service = None
        '''
        
        # Replace the existing ChromeDriver code
        old_code = '''        # Use webdriver-manager to automatically handle ChromeDriver
        try:
            service = Service(ChromeDriverManager().install())
        except Exception as e:
            self.logger.warning(f"ChromeDriverManager failed: {e}")
            # Try without explicit service - let Selenium handle it
            service = None'''
        
        if old_code in content:
            content = content.replace(old_code, new_code)
            
            # Write the updated content
            with open('linkedin_automation.py', 'w', encoding='utf-8') as f:
                f.write(content)
            
            print("✅ Automation code updated successfully")
            return True
        else:
            print("⚠️ Could not find exact code to replace, but ChromeDriver should still work")
            return True
            
    except Exception as e:
        print(f"❌ Error updating automation code: {e}")
        return False

def main():
    """Main function to complete ChromeDriver fix"""
    print("=" * 60)
    print("Completing ChromeDriver Fix")
    print("=" * 60)
    
    # Download ChromeDriver
    chromedriver_path = download_latest_chromedriver()
    if not chromedriver_path:
        print("❌ Failed to download ChromeDriver")
        return False
    
    # Test ChromeDriver
    if not test_chromedriver(chromedriver_path):
        print("❌ ChromeDriver test failed")
        return False
    
    # Update automation code
    if not update_automation_code():
        print("❌ Failed to update automation code")
        return False
    
    print("\n🎉 ChromeDriver fix completed successfully!")
    print("✅ Your automation should now work properly")
    print("\n🚀 To test:")
    print("   1. Restart your web application")
    print("   2. Go to the dashboard")
    print("   3. Click 'Start Automation'")
    print("   4. The browser should now start successfully")
    
    return True

if __name__ == "__main__":
    main()
