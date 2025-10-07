"""
Integration tests for the LinkedIn automation MVP
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from linkedin_automation import LinkedInAutomation
from config import LinkedInConfig, JobApplicationConfig


class TestLinkedInAutomationIntegration:
    """Integration tests for the complete automation workflow"""
    
    @pytest.fixture
    def mock_config(self):
        """Create mock configuration for integration testing"""
        return LinkedInConfig(
            email="integration@example.com",
            password="integrationpassword",
            job_keywords=["Data Analyst", "Business Analyst"],
            easy_apply_only=True,
            max_applications_per_day=3
        )
    
    @pytest.fixture
    def mock_job_config(self):
        """Create mock job configuration for integration testing"""
        return JobApplicationConfig(
            auto_apply=True,
            send_messages=True,
            message_template="Hello, I'm interested in this position."
        )
    
    @pytest.fixture
    def automation(self, mock_config, mock_job_config):
        """Create LinkedInAutomation instance for integration testing"""
        return LinkedInAutomation(mock_config, mock_job_config)
    
    @patch('linkedin_automation.webdriver.Chrome')
    @patch('linkedin_automation.Service')
    @patch('linkedin_automation.ChromeDriverManager')
    @patch('linkedin_automation.WebDriverWait')
    def test_complete_workflow_success(self, mock_wait_class, mock_driver_manager, 
                                     mock_service, mock_chrome, automation):
        """Test complete automation workflow from start to finish"""
        # Setup mocks
        mock_driver = Mock()
        mock_wait = Mock()
        mock_wait_class.return_value = mock_wait
        mock_driver_manager.install.return_value = "/path/to/chromedriver"
        
        automation.driver = mock_driver
        automation.wait = mock_wait
        
        # Mock login elements
        mock_email_field = Mock()
        mock_password_field = Mock()
        mock_login_button = Mock()
        
        # Mock job search elements
        mock_search_box = Mock()
        mock_filter_button = Mock()
        
        # Mock job listings
        mock_job_element = Mock()
        mock_title_element = Mock()
        mock_company_element = Mock()
        mock_easy_apply_button = Mock()
        
        mock_title_element.text = "Senior Data Analyst"
        mock_company_element.text = "Tech Corp"
        
        mock_job_element.find_element.side_effect = [
            mock_title_element,
            mock_company_element,
            mock_easy_apply_button
        ]
        
        # Mock application form elements
        mock_submit_button = Mock()
        mock_success_indicator = Mock()
        
        # Configure mock wait calls
        mock_wait.until.side_effect = [
            mock_email_field,  # Login email field
            Mock(),  # Login verification
            mock_search_box,  # Job search box
            mock_filter_button,  # Easy Apply filter
            mock_submit_button,  # Application submit button
            mock_success_indicator  # Success verification
        ]
        
        mock_driver.find_element.side_effect = [
            mock_password_field,  # Login password field
            mock_login_button,  # Login button
            mock_submit_button,  # Application submit button
            mock_success_indicator  # Success indicator
        ]
        
        mock_driver.find_elements.return_value = [mock_job_element]
        
        # Execute workflow
        # 1. Start session
        result = automation.start_session()
        assert result is True
        
        # 2. Login
        result = automation.login()
        assert result is True
        
        # 3. Search jobs
        result = automation.search_jobs()
        assert result is True
        
        # 4. Get job listings
        jobs = automation.get_job_listings(max_jobs=1)
        assert len(jobs) == 1
        assert jobs[0]['title'] == "Senior Data Analyst"
        assert jobs[0]['company'] == "Tech Corp"
        assert jobs[0]['has_easy_apply'] is True
        
        # 5. Apply to job
        result = automation.apply_to_job(jobs[0])
        assert result is True
        assert automation.applications_today == 1
        
        # 6. Check stats
        stats = automation.get_application_stats()
        assert stats['applications_today'] == 1
        assert stats['remaining_applications'] == 2
        
        # 7. Close session
        automation.close_session()
        mock_driver.quit.assert_called_once()
    
    @patch('linkedin_automation.webdriver.Chrome')
    @patch('linkedin_automation.Service')
    @patch('linkedin_automation.ChromeDriverManager')
    @patch('linkedin_automation.WebDriverWait')
    def test_workflow_with_multiple_applications(self, mock_wait_class, mock_driver_manager,
                                               mock_service, mock_chrome, automation):
        """Test workflow with multiple job applications"""
        # Setup mocks
        mock_driver = Mock()
        mock_wait = Mock()
        mock_wait_class.return_value = mock_wait
        
        automation.driver = mock_driver
        automation.wait = mock_wait
        
        # Mock multiple job elements
        mock_job1 = Mock()
        mock_job2 = Mock()
        mock_job3 = Mock()
        
        # Setup job 1
        mock_title1 = Mock()
        mock_company1 = Mock()
        mock_title1.text = "Data Analyst"
        mock_company1.text = "Company A"
        mock_job1.find_element.side_effect = [mock_title1, mock_company1, Mock()]
        
        # Setup job 2
        mock_title2 = Mock()
        mock_company2 = Mock()
        mock_title2.text = "Business Analyst"
        mock_company2.text = "Company B"
        mock_job2.find_element.side_effect = [mock_title2, mock_company2, Mock()]
        
        # Setup job 3 (no Easy Apply)
        mock_title3 = Mock()
        mock_company3 = Mock()
        mock_title3.text = "Data Scientist"
        mock_company3.text = "Company C"
        mock_job3.find_element.side_effect = [
            mock_title3, 
            mock_company3, 
            NoSuchElementException("No Easy Apply button")
        ]
        
        mock_driver.find_elements.return_value = [mock_job1, mock_job2, mock_job3]
        
        # Mock application form elements
        mock_submit_button = Mock()
        mock_success_indicator = Mock()
        
        mock_wait.until.return_value = mock_submit_button
        mock_driver.find_element.side_effect = [
            mock_submit_button,
            mock_success_indicator,
            mock_submit_button,
            mock_success_indicator
        ]
        
        # Get job listings
        jobs = automation.get_job_listings(max_jobs=3)
        assert len(jobs) == 3
        
        # Apply to jobs with Easy Apply
        easy_apply_jobs = [job for job in jobs if job['has_easy_apply']]
        assert len(easy_apply_jobs) == 2
        
        # Apply to first job
        result1 = automation.apply_to_job(easy_apply_jobs[0])
        assert result1 is True
        assert automation.applications_today == 1
        
        # Apply to second job
        result2 = automation.apply_to_job(easy_apply_jobs[1])
        assert result2 is True
        assert automation.applications_today == 2
        
        # Try to apply to job without Easy Apply
        no_easy_apply_jobs = [job for job in jobs if not job['has_easy_apply']]
        result3 = automation.apply_to_job(no_easy_apply_jobs[0])
        assert result3 is False
        assert automation.applications_today == 2  # Should not increment
    
    @patch('linkedin_automation.webdriver.Chrome')
    @patch('linkedin_automation.Service')
    @patch('linkedin_automation.ChromeDriverManager')
    @patch('linkedin_automation.WebDriverWait')
    def test_workflow_with_daily_limit(self, mock_wait_class, mock_driver_manager,
                                     mock_service, mock_chrome, automation):
        """Test workflow respecting daily application limits"""
        # Setup mocks
        mock_driver = Mock()
        mock_wait = Mock()
        mock_wait_class.return_value = mock_wait
        
        automation.driver = mock_driver
        automation.wait = mock_wait
        
        # Set applications to near limit
        automation.applications_today = 2  # Max is 3
        
        # Mock job elements
        mock_job = Mock()
        mock_title = Mock()
        mock_company = Mock()
        mock_title.text = "Data Analyst"
        mock_company.text = "Test Company"
        mock_job.find_element.side_effect = [mock_title, mock_company, Mock()]
        
        mock_driver.find_elements.return_value = [mock_job]
        
        # Mock application form elements
        mock_submit_button = Mock()
        mock_success_indicator = Mock()
        
        mock_wait.until.return_value = mock_submit_button
        mock_driver.find_element.side_effect = [
            mock_submit_button,
            mock_success_indicator
        ]
        
        # Get job listings
        jobs = automation.get_job_listings(max_jobs=1)
        
        # Apply to job (should succeed - 3rd application)
        result1 = automation.apply_to_job(jobs[0])
        assert result1 is True
        assert automation.applications_today == 3
        
        # Try to apply to another job (should fail - limit reached)
        result2 = automation.apply_to_job(jobs[0])
        assert result2 is False
        assert automation.applications_today == 3  # Should not increment
    
    @patch('linkedin_automation.webdriver.Chrome')
    @patch('linkedin_automation.Service')
    @patch('linkedin_automation.ChromeDriverManager')
    @patch('linkedin_automation.WebDriverWait')
    def test_workflow_with_messaging(self, mock_wait_class, mock_driver_manager,
                                   mock_service, mock_chrome, automation):
        """Test workflow including messaging functionality"""
        # Setup mocks
        mock_driver = Mock()
        mock_wait = Mock()
        mock_wait_class.return_value = mock_wait
        
        automation.driver = mock_driver
        automation.wait = mock_wait
        
        # Mock message elements
        mock_message_field = Mock()
        mock_send_button = Mock()
        
        mock_wait.until.return_value = mock_message_field
        mock_driver.find_element.return_value = mock_send_button
        
        # Test sending message
        result = automation.send_message(
            "Hello, I'm interested in this position.",
            "https://www.linkedin.com/messaging/thread/test/"
        )
        
        assert result is True
        mock_driver.get.assert_called_with("https://www.linkedin.com/messaging/thread/test/")
        mock_message_field.clear.assert_called_once()
        mock_message_field.send_keys.assert_called_with("Hello, I'm interested in this position.")
        mock_send_button.click.assert_called_once()
    
    def test_error_handling_workflow(self, automation):
        """Test error handling throughout the workflow"""
        # Test without starting session
        assert automation.login() is False
        assert automation.search_jobs() is False
        assert automation.get_job_listings() == []
        assert automation.apply_to_job({}) is False
        assert automation.send_message("test") is False
        
        # Test with mock driver but no proper setup
        automation.driver = Mock()
        automation.wait = Mock()
        
        # Mock timeout exceptions
        automation.wait.until.side_effect = TimeoutException("Element not found")
        
        assert automation.login() is False
        assert automation.search_jobs() is False
