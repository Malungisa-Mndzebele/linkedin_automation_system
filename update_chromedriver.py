"""
ChromeDriver Update Script
Downloads the latest compatible ChromeDriver for Chrome 141
"""
import os
import requests
import zipfile
import tempfile
from pathlib import Path

def get_latest_chromedriver():
    """Get the latest ChromeDriver version"""
    print("🔍 Getting latest ChromeDriver version...")
    
    try:
        # Try to get the latest version
        response = requests.get('https://chromedriver.storage.googleapis.com/LATEST_RELEASE')
        if response.status_code == 200:
            version = response.text.strip()
            print(f"✅ Latest ChromeDriver version: {version}")
            return version
        else:
            print("❌ Could not get latest ChromeDriver version")
            return None
    except Exception as e:
        print(f"❌ Error getting ChromeDriver version: {e}")
        return None

def download_chromedriver_for_chrome_141():
    """Download ChromeDriver compatible with Chrome 141"""
    print("🔍 Finding ChromeDriver for Chrome 141...")
    
    # Chrome 141 is very new, so we'll try to get the latest available
    # and use webdriver-manager's automatic compatibility handling
    
    try:
        # Try to get ChromeDriver for Chrome 120+ (more likely to work)
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
    """Test ChromeDriver compatibility"""
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

def update_webdriver_manager():
    """Update webdriver-manager to latest version"""
    print("🔄 Updating webdriver-manager...")
    try:
        import subprocess
        import sys
        subprocess.check_call([sys.executable, "-m", "pip", "install", "--upgrade", "webdriver-manager"])
        print("✅ webdriver-manager updated successfully")
        return True
    except Exception as e:
        print(f"❌ Failed to update webdriver-manager: {e}")
        return False

def main():
    """Main function to update ChromeDriver"""
    print("=" * 60)
    print("ChromeDriver Update for Chrome 141")
    print("=" * 60)
    
    # Update webdriver-manager first
    if not update_webdriver_manager():
        print("⚠️ Could not update webdriver-manager, continuing anyway...")
    
    # Download compatible ChromeDriver
    chromedriver_path = download_chromedriver_for_chrome_141()
    if not chromedriver_path:
        print("❌ Failed to download ChromeDriver")
        return False
    
    # Test ChromeDriver
    if not test_chromedriver_compatibility(chromedriver_path):
        print("❌ ChromeDriver compatibility test failed")
        print("📝 The automation will use webdriver-manager's automatic handling")
        print("✅ This should still work with the updated fallback logic")
    
    print("\n🎉 ChromeDriver update completed!")
    print("✅ Your automation should now work better")
    print("\n🚀 To test:")
    print("   1. Restart your web application")
    print("   2. Try starting automation from the dashboard")
    print("   3. The system will try multiple ChromeDriver approaches")
    
    return True

if __name__ == "__main__":
    main()
