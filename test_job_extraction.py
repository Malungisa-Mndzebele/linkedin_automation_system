"""
Test script to verify job extraction functionality
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from linkedin_automation import LinkedInAutomation
from config import LinkedInConfig, JobApplicationConfig


def test_job_extraction():
    """Test job extraction with updated selectors"""
    print("Testing job extraction with updated selectors...")
    
    # Create test configuration
    config = LinkedInConfig(
        email="test@example.com",
        password="testpassword",
        job_keywords=["Data Analyst"],
        easy_apply_only=True,
        headless=False,
        implicit_wait=10,
        page_load_timeout=30
    )
    job_config = JobApplicationConfig()
    
    # Initialize automation
    automation = LinkedInAutomation(config, job_config)
    
    try:
        # Test driver setup
        print("Setting up Chrome driver...")
        driver = automation._setup_driver()
        print("[SUCCESS] Chrome driver setup successful!")
        
        # Navigate to LinkedIn job search
        print("Navigating to LinkedIn job search...")
        search_url = "https://www.linkedin.com/jobs/search/?keywords=Data%20Analyst&f_LF=f_AL"
        driver.get(search_url)
        print("[SUCCESS] LinkedIn job search page loaded!")
        
        # Wait for page to load
        import time
        time.sleep(8)  # Give more time for content to load
        
        # Test job extraction with debug info
        print("Testing job extraction with debug information...")
        jobs = automation.get_job_listings(max_jobs=3)
        
        if jobs:
            print(f"[SUCCESS] Found {len(jobs)} job listings!")
            for i, job in enumerate(jobs, 1):
                print(f"  Job {i}: {job['title']} at {job['company']} - Easy Apply: {job['has_easy_apply']}")
        else:
            print("[INFO] No job listings extracted - check logs for debug information")
        
        # Close driver
        driver.quit()
        print("[SUCCESS] Driver cleanup successful!")
        
        print("\n*** Job extraction test completed! ***")
        print("Check the logs for detailed debug information if extraction failed.")
        return True
        
    except Exception as e:
        print(f"[FAILED] Job extraction test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_job_extraction()
    sys.exit(0 if success else 1)
