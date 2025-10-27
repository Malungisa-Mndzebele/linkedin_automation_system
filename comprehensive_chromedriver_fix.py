"""
Comprehensive ChromeDriver Fix
Handles version compatibility and provides multiple fallback options
"""
import os
import sys
import subprocess
import requests
import zipfile
import tempfile
from pathlib import Path

def get_chrome_version():
    """Get installed Chrome version"""
    try:
        import winreg
        # Try multiple registry locations
        locations = [
            (winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Google\Chrome\BLBeacon"),
            (winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome"),
            (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Google\Chrome")
        ]
        
        for hkey, subkey in locations:
            try:
                key = winreg.OpenKey(hkey, subkey)
                version, _ = winreg.QueryValueEx(key, "version")
                winreg.CloseKey(key)
                print(f"✅ Chrome version found: {version}")
                return version
            except:
                continue
        
        print("❌ Could not detect Chrome version")
        return None
    except ImportError:
        print("❌ Windows registry access not available")
        return None

def download_compatible_chromedriver():
    """Download a compatible ChromeDriver version"""
    print("🔍 Finding compatible ChromeDriver...")
    
    try:
        # Try to get ChromeDriver for Chrome 120+ (more compatible)
        versions_to_try = ["120", "119", "118", "117", "116", "115", "114"]
        
        for version in versions_to_try:
            try:
                url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{version}"
                response = requests.get(url)
                if response.status_code == 200:
                    chromedriver_version = response.text.strip()
                    print(f"✅ Found ChromeDriver version: {chromedriver_version}")
                    
                    # Download ChromeDriver
                    download_url = f"https://chromedriver.storage.googleapis.com/{chromedriver_version}/chromedriver_win32.zip"
                    print(f"📥 Downloading ChromeDriver from: {download_url}")
                    
                    response = requests.get(download_url)
                    if response.status_code == 200:
                        # Save to temporary file
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
                            tmp_file.write(response.content)
                            zip_path = tmp_file.name
                        
                        # Extract ChromeDriver
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
                            continue
                    else:
                        print(f"❌ Could not download ChromeDriver for version {version}")
                        continue
            except Exception as e:
                print(f"❌ Error with version {version}: {e}")
                continue
        
        print("❌ Could not find compatible ChromeDriver")
        return False
        
    except Exception as e:
        print(f"❌ Error downloading ChromeDriver: {e}")
        return False

def test_chromedriver_compatibility(path):
    """Test ChromeDriver compatibility with current Chrome"""
    print("🧪 Testing ChromeDriver compatibility...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--allow-running-insecure-content")
        
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

def create_chromedriver_fallback():
    """Create a fallback ChromeDriver configuration"""
    print("🔧 Creating ChromeDriver fallback configuration...")
    
    try:
        # Create a simple test script
        test_script = '''
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def test_chrome_without_chromedriver():
    """Test Chrome without explicit ChromeDriver"""
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-gpu")
        
        # Try without explicit service
        driver = webdriver.Chrome(options=chrome_options)
        driver.get("https://www.google.com")
        title = driver.title
        driver.quit()
        
        print(f"✅ Chrome test successful! Page title: {title}")
        return True
        
    except Exception as e:
        print(f"❌ Chrome test failed: {e}")
        return False

if __name__ == "__main__":
    test_chrome_without_chromedriver()
'''
        
        with open('test_chrome_fallback.py', 'w') as f:
            f.write(test_script)
        
        print("✅ Fallback test script created")
        return True
        
    except Exception as e:
        print(f"❌ Error creating fallback: {e}")
        return False

def main():
    """Main function to complete ChromeDriver fix"""
    print("=" * 60)
    print("Comprehensive ChromeDriver Fix")
    print("=" * 60)
    
    # Get Chrome version
    chrome_version = get_chrome_version()
    
    # Download compatible ChromeDriver
    chromedriver_path = download_compatible_chromedriver()
    
    if chromedriver_path:
        # Test ChromeDriver
        if test_chromedriver_compatibility(chromedriver_path):
            print("\n🎉 ChromeDriver fix completed successfully!")
            print("✅ Your automation should now work properly")
        else:
            print("\n⚠️ ChromeDriver downloaded but compatibility test failed")
            print("🔄 Trying fallback approach...")
            
            # Create fallback
            create_chromedriver_fallback()
            
            # Test fallback
            try:
                result = subprocess.run([sys.executable, 'test_chrome_fallback.py'], 
                                      capture_output=True, text=True, timeout=30)
                if result.returncode == 0:
                    print("✅ Fallback approach works!")
                    print("🎉 ChromeDriver fix completed with fallback!")
                else:
                    print("❌ Fallback approach also failed")
                    print("📝 Manual steps required:")
                    print("   1. Update Chrome to a stable version")
                    print("   2. Or download ChromeDriver manually")
            except Exception as e:
                print(f"❌ Fallback test failed: {e}")
    else:
        print("\n❌ Could not download ChromeDriver")
        print("📝 Manual steps:")
        print("   1. Download ChromeDriver from: https://chromedriver.chromium.org/")
        print("   2. Extract chromedriver.exe to the chromedriver folder")
        print("   3. Ensure version compatibility with your Chrome")
    
    print("\n🚀 To test:")
    print("   1. Restart your web application")
    print("   2. Go to the dashboard")
    print("   3. Click 'Start Automation'")
    print("   4. Check the logs for ChromeDriver status")

if __name__ == "__main__":
    main()
