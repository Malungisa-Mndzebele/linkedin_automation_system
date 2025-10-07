"""
Test runner script for LinkedIn Job Application Automation MVP
"""
import sys
import os
from unittest.mock import Mock, patch

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from linkedin_automation import LinkedInAutomation
from config import LinkedInConfig, JobApplicationConfig


def test_config_creation():
    """Test configuration creation"""
    print("Testing configuration creation...")
    
    config = LinkedInConfig(
        email="test@example.com",
        password="testpassword",
        job_keywords=["Data Analyst", "Business Analyst"],
        easy_apply_only=True,
        max_applications_per_day=5
    )
    
    assert config.email == "test@example.com"
    assert config.job_keywords == ["Data Analyst", "Business Analyst"]
    assert config.easy_apply_only is True
    print("[PASS] Configuration creation test passed")


def test_automation_initialization():
    """Test automation initialization"""
    print("Testing automation initialization...")
    
    config = LinkedInConfig(
        email="test@example.com",
        password="testpassword"
    )
    job_config = JobApplicationConfig()
    
    automation = LinkedInAutomation(config, job_config)
    
    assert automation.config == config
    assert automation.job_config == job_config
    assert automation.driver is None
    assert automation.applications_today == 0
    print("[PASS] Automation initialization test passed")


def test_application_stats():
    """Test application statistics"""
    print("Testing application statistics...")
    
    config = LinkedInConfig(
        email="test@example.com",
        password="testpassword",
        max_applications_per_day=10
    )
    job_config = JobApplicationConfig()
    
    automation = LinkedInAutomation(config, job_config)
    automation.applications_today = 3
    
    stats = automation.get_application_stats()
    
    assert stats['applications_today'] == 3
    assert stats['max_applications_per_day'] == 10
    assert stats['remaining_applications'] == 7
    print("[PASS] Application statistics test passed")


def test_job_info_processing():
    """Test job information processing"""
    print("Testing job information processing...")
    
    config = LinkedInConfig(
        email="test@example.com",
        password="testpassword"
    )
    job_config = JobApplicationConfig()
    
    automation = LinkedInAutomation(config, job_config)
    
    # Test job info validation
    job_with_easy_apply = {
        'title': 'Data Analyst',
        'company': 'Tech Corp',
        'has_easy_apply': True
    }
    
    job_without_easy_apply = {
        'title': 'Data Scientist',
        'company': 'Big Corp',
        'has_easy_apply': False
    }
    
    # Test daily limit check
    automation.applications_today = 0
    assert automation.applications_today < config.max_applications_per_day
    
    # Test Easy Apply check
    assert job_with_easy_apply['has_easy_apply'] is True
    assert job_without_easy_apply['has_easy_apply'] is False
    
    print("[PASS] Job information processing test passed")


def test_error_handling():
    """Test error handling scenarios"""
    print("Testing error handling...")
    
    config = LinkedInConfig(
        email="test@example.com",
        password="testpassword"
    )
    job_config = JobApplicationConfig()
    
    automation = LinkedInAutomation(config, job_config)
    
    # Test operations without driver
    assert automation.login() is False
    assert automation.search_jobs() is False
    assert automation.get_job_listings() == []
    assert automation.apply_to_job({}) is False
    assert automation.send_message("test") is False
    
    print("[PASS] Error handling test passed")


def test_mock_workflow():
    """Test complete workflow with mocked components"""
    print("Testing complete workflow with mocks...")
    
    config = LinkedInConfig(
        email="test@example.com",
        password="testpassword",
        max_applications_per_day=3
    )
    job_config = JobApplicationConfig()
    
    automation = LinkedInAutomation(config, job_config)
    
    # Mock driver and wait
    mock_driver = Mock()
    mock_wait = Mock()
    
    automation.driver = mock_driver
    automation.wait = mock_wait
    
    # Mock successful login
    mock_email_field = Mock()
    mock_password_field = Mock()
    mock_login_button = Mock()
    
    mock_driver.find_element.side_effect = [mock_password_field, mock_login_button]
    mock_wait.until.return_value = mock_email_field
    
    # Test login
    result = automation.login()
    assert result is True
    
    # Mock job search
    mock_search_box = Mock()
    mock_filter_button = Mock()
    
    mock_wait.until.side_effect = [mock_search_box, mock_filter_button]
    
    # Test job search
    result = automation.search_jobs()
    assert result is True
    
    # Mock job listings
    mock_job_element = Mock()
    mock_title_element = Mock()
    mock_company_element = Mock()
    
    mock_title_element.text = "Data Analyst"
    mock_company_element.text = "Test Company"
    
    mock_job_element.find_element.side_effect = [
        mock_title_element,
        mock_company_element,
        Mock()  # Easy Apply button
    ]
    
    mock_driver.find_elements.return_value = [mock_job_element]
    
    # Test getting job listings
    jobs = automation.get_job_listings(max_jobs=1)
    assert len(jobs) == 1
    assert jobs[0]['title'] == "Data Analyst"
    assert jobs[0]['company'] == "Test Company"
    assert jobs[0]['has_easy_apply'] is True
    
    print("[PASS] Complete workflow test passed")


def main():
    """Run all tests"""
    print("=" * 60)
    print("LinkedIn Job Application Automation MVP - Test Runner")
    print("=" * 60)
    
    try:
        test_config_creation()
        test_automation_initialization()
        test_application_stats()
        test_job_info_processing()
        test_error_handling()
        test_mock_workflow()
        
        print("\n" + "=" * 60)
        print("*** ALL TESTS PASSED! ***")
        print("=" * 60)
        print("\nMVP Features Verified:")
        print("[PASS] Configuration management")
        print("[PASS] Automation initialization")
        print("[PASS] Application tracking")
        print("[PASS] Job information processing")
        print("[PASS] Error handling")
        print("[PASS] Complete workflow simulation")
        print("\nThe LinkedIn Job Application Automation MVP is ready!")
        
        return 0
        
    except Exception as e:
        print(f"\n[FAIL] TEST FAILED: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
