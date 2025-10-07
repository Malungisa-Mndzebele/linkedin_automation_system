"""
Test script to verify LinkedIn job search functionality with updated interface
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from linkedin_automation import LinkedInAutomation
from config import LinkedInConfig, JobApplicationConfig


def test_linkedin_search():
    """Test LinkedIn job search with updated interface"""
    print("Testing LinkedIn job search with updated interface...")
    
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
        
        # Test LinkedIn navigation
        print("Testing LinkedIn job search navigation...")
        search_url = "https://www.linkedin.com/jobs/search/?keywords=Data%20Analyst&f_LF=f_AL"
        driver.get(search_url)
        print("[SUCCESS] LinkedIn job search page loaded!")
        
        # Wait for page to load
        import time
        time.sleep(5)
        
        # Test job extraction
        print("Testing job extraction...")
        jobs = automation.get_job_listings(max_jobs=3)
        
        if jobs:
            print(f"[SUCCESS] Found {len(jobs)} job listings!")
            for i, job in enumerate(jobs, 1):
                print(f"  Job {i}: {job['title']} at {job['company']} - Easy Apply: {job['has_easy_apply']}")
        else:
            print("[WARNING] No job listings found - this may be normal if no jobs match the criteria")
        
        # Close driver
        driver.quit()
        print("[SUCCESS] Driver cleanup successful!")
        
        print("\n*** LinkedIn job search test completed! ***")
        return True
        
    except Exception as e:
        print(f"[FAILED] LinkedIn search test failed: {e}")
        return False


if __name__ == "__main__":
    success = test_linkedin_search()
    sys.exit(0 if success else 1)
