"""
ChromeDriver Installation and Fix Script
Resolves ChromeDriver compatibility issues on Windows
"""
import os
import sys
import subprocess
import requests
import zipfile
import tempfile
from pathlib import Path

def check_chrome_version():
    """Check installed Chrome version"""
    try:
        # Try to get Chrome version from registry (Windows)
        import winreg
        key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Software\Google\Chrome\BLBeacon")
        version, _ = winreg.QueryValueEx(key, "version")
        winreg.CloseKey(key)
        print(f"✅ Chrome version found: {version}")
        return version
    except:
        try:
            # Try alternative registry location
            import winreg
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Google\Chrome\BLBeacon")
            version, _ = winreg.QueryValueEx(key, "version")
            winreg.CloseKey(key)
            print(f"✅ Chrome version found: {version}")
            return version
        except:
            print("❌ Could not detect Chrome version")
            return None

def download_chromedriver(version):
    """Download appropriate ChromeDriver version"""
    try:
        # Get major version number
        major_version = version.split('.')[0]
        
        # ChromeDriver download URL
        url = f"https://chromedriver.storage.googleapis.com/LATEST_RELEASE_{major_version}"
        
        print(f"🔍 Checking ChromeDriver for Chrome {major_version}...")
        
        # Get latest ChromeDriver version
        response = requests.get(url)
        if response.status_code == 200:
            chromedriver_version = response.text.strip()
            print(f"✅ Latest ChromeDriver version: {chromedriver_version}")
        else:
            print("❌ Could not get ChromeDriver version")
            return False
        
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
            extract_dir = Path.cwd() / "chromedriver"
            extract_dir.mkdir(exist_ok=True)
            
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
            
            # Clean up
            os.unlink(zip_path)
            
            chromedriver_path = extract_dir / "chromedriver.exe"
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

def fix_chromedriver_issue():
    """Fix ChromeDriver compatibility issue"""
    print("=" * 60)
    print("ChromeDriver Installation and Fix Script")
    print("=" * 60)
    
    # Check Chrome version
    chrome_version = check_chrome_version()
    if not chrome_version:
        print("❌ Chrome not found. Please install Google Chrome first.")
        return False
    
    # Download ChromeDriver
    chromedriver_path = download_chromedriver(chrome_version)
    if not chromedriver_path:
        print("❌ Failed to install ChromeDriver")
        return False
    
    # Test ChromeDriver
    print("🧪 Testing ChromeDriver...")
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        service = Service(chromedriver_path)
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

def update_webdriver_manager():
    """Update webdriver-manager to latest version"""
    print("🔄 Updating webdriver-manager...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "webdriver-manager"])
        print("✅ webdriver-manager updated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to update webdriver-manager: {e}")
        return False

def main():
    """Main function"""
    print("🔧 Fixing ChromeDriver compatibility issue...")
    
    # Update webdriver-manager first
    if not update_webdriver_manager():
        print("⚠️ Could not update webdriver-manager, continuing anyway...")
    
    # Fix ChromeDriver issue
    if fix_chromedriver_issue():
        print("\n🎉 ChromeDriver issue fixed successfully!")
        print("✅ Your web application should now work properly")
        print("\n🚀 To test:")
        print("   1. Restart your web application")
        print("   2. Try starting automation from the dashboard")
    else:
        print("\n❌ Could not fix ChromeDriver issue automatically")
        print("📝 Manual steps:")
        print("   1. Download ChromeDriver from: https://chromedriver.chromium.org/")
        print("   2. Extract chromedriver.exe to your project folder")
        print("   3. Ensure ChromeDriver version matches your Chrome version")

if __name__ == "__main__":
    main()
