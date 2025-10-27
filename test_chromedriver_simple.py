"""
Simple ChromeDriver Test
Tests ChromeDriver functionality without Unicode characters
"""
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
            
            print(f"SUCCESS: {approach_name} worked! Page title: {title}")
            return True
            
        except Exception as e:
            print(f"FAILED: {approach_name} failed: {e}")
            continue
    
    print("ERROR: All approaches failed")
    return False

if __name__ == "__main__":
    success = test_chromedriver()
    sys.exit(0 if success else 1)
