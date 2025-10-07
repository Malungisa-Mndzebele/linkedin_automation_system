"""
Unit tests for LinkedIn automation functionality
"""
import pytest
from unittest.mock import Mock, patch, MagicMock
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException

from linkedin_automation import LinkedInAutomation
from config import LinkedInConfig, JobApplicationConfig


class TestLinkedInAutomation:
    """Test cases for LinkedInAutomation class"""
    
    @pytest.fixture
    def mock_config(self):
        """Create mock configuration for testing"""
        return LinkedInConfig(
            email="test@example.com",
            password="testpassword",
            job_keywords=["Data Analyst"],
            easy_apply_only=True,
            max_applications_per_day=5
        )
    
    @pytest.fixture
    def mock_job_config(self):
        """Create mock job configuration for testing"""
        return JobApplicationConfig()
    
    @pytest.fixture
    def automation(self, mock_config, mock_job_config):
        """Create LinkedInAutomation instance for testing"""
        return LinkedInAutomation(mock_config, mock_job_config)
    
    def test_automation_initialization(self, automation, mock_config, mock_job_config):
        """Test LinkedInAutomation initialization"""
        assert automation.config == mock_config
        assert automation.job_config == mock_job_config
        assert automation.driver is None
        assert automation.wait is None
        assert automation.applications_today == 0
        assert automation.logger is not None
    
    @patch('linkedin_automation.webdriver.Chrome')
    @patch('linkedin_automation.Service')
    @patch('linkedin_automation.ChromeDriverManager')
    def test_setup_driver_success(self, mock_driver_manager, mock_service, mock_chrome, automation):
        """Test successful driver setup"""
        # Mock the ChromeDriverManager
        mock_driver_manager.install.return_value = "/path/to/chromedriver"
        
        # Mock the Service
        mock_service_instance = Mock()
        mock_service.return_value = mock_service_instance
        
        # Mock the Chrome driver
        mock_driver_instance = Mock()
        mock_chrome.return_value = mock_driver_instance
        
        # Call the method
        result = automation._setup_driver()
        
        # Assertions
        assert result == mock_driver_instance
        mock_driver_manager.install.assert_called_once()
        mock_service.assert_called_once_with("/path/to/chromedriver")
        mock_chrome.assert_called_once()
        mock_driver_instance.execute_script.assert_called()
        mock_driver_instance.implicitly_wait.assert_called_with(10)
        mock_driver_instance.set_page_load_timeout.assert_called_with(30)
    
    @patch('linkedin_automation.webdriver.Chrome')
    def test_setup_driver_failure(self, mock_chrome, automation):
        """Test driver setup failure"""
        mock_chrome.side_effect = WebDriverException("Driver setup failed")
        
        with pytest.raises(WebDriverException):
            automation._setup_driver()
    
    @patch.object(LinkedInAutomation, '_setup_driver')
    def test_start_session_success(self, mock_setup_driver, automation):
        """Test successful session start"""
        mock_driver = Mock()
        mock_setup_driver.return_value = mock_driver
        
        result = automation.start_session()
        
        assert result is True
        assert automation.driver == mock_driver
        assert automation.wait is not None
        mock_driver.maximize_window.assert_called_once()
        # Note: implicitly_wait and set_page_load_timeout are called in _setup_driver, not start_session
    
    @patch.object(LinkedInAutomation, '_setup_driver')
    def test_start_session_failure(self, mock_setup_driver, automation):
        """Test session start failure"""
        mock_setup_driver.side_effect = Exception("Setup failed")
        
        result = automation.start_session()
        
        assert result is False
        assert automation.driver is None
        assert automation.wait is None
    
    def test_login_without_driver(self, automation):
        """Test login without initialized driver"""
        result = automation.login()
        assert result is False
    
    @patch('linkedin_automation.WebDriverWait')
    def test_login_success(self, mock_wait_class, automation):
        """Test successful login"""
        # Setup mocks
        mock_driver = Mock()
        mock_wait = Mock()
        mock_wait_class.return_value = mock_wait
        
        automation.driver = mock_driver
        automation.wait = mock_wait
        
        # Mock elements
        mock_email_field = Mock()
        mock_password_field = Mock()
        mock_login_button = Mock()
        
        mock_driver.find_element.side_effect = [mock_password_field, mock_login_button]
        mock_wait.until.return_value = mock_email_field
        
        # Mock successful login verification
        mock_wait.until.side_effect = [
            mock_email_field,  # First call for email field
            Mock()  # Second call for login verification
        ]
        
        result = automation.login()
        
        assert result is True
        mock_driver.get.assert_called_with("https://www.linkedin.com/login")
        mock_email_field.clear.assert_called_once()
        mock_email_field.send_keys.assert_called_with("test@example.com")
        mock_password_field.clear.assert_called_once()
        mock_password_field.send_keys.assert_called_with("testpassword")
        mock_login_button.click.assert_called_once()
    
    @patch('linkedin_automation.WebDriverWait')
    def test_login_timeout(self, mock_wait_class, automation):
        """Test login timeout"""
        mock_driver = Mock()
        mock_wait = Mock()
        mock_wait_class.return_value = mock_wait
        
        automation.driver = mock_driver
        automation.wait = mock_wait
        
        # Mock elements
        mock_email_field = Mock()
        mock_password_field = Mock()
        mock_login_button = Mock()
        
        mock_driver.find_element.side_effect = [mock_password_field, mock_login_button]
        mock_wait.until.side_effect = [
            mock_email_field,  # First call for email field
            TimeoutException("Login verification timeout")  # Second call for login verification
        ]
        
        result = automation.login()
        
        assert result is False
    
    def test_search_jobs_without_driver(self, automation):
        """Test job search without initialized driver"""
        result = automation.search_jobs()
        assert result is False
    
    @patch('linkedin_automation.WebDriverWait')
    def test_search_jobs_success(self, mock_wait_class, automation):
        """Test successful job search"""
        mock_driver = Mock()
        mock_wait = Mock()
        mock_wait_class.return_value = mock_wait
        
        automation.driver = mock_driver
        automation.wait = mock_wait
        
        # Mock search box
        mock_search_box = Mock()
        mock_wait.until.return_value = mock_search_box
        
        # Mock Easy Apply filter
        mock_filter_button = Mock()
        mock_wait.until.side_effect = [
            mock_search_box,  # First call for search box
            mock_filter_button  # Second call for Easy Apply filter
        ]
        
        result = automation.search_jobs()
        
        assert result is True
        mock_driver.get.assert_called_with("https://www.linkedin.com/jobs/")
        mock_search_box.clear.assert_called_once()
        # The search term is sent first, then Keys.RETURN
        mock_search_box.send_keys.assert_any_call("Data Analyst")
        mock_filter_button.click.assert_called_once()
    
    def test_get_job_listings_without_driver(self, automation):
        """Test getting job listings without driver"""
        result = automation.get_job_listings()
        assert result == []
    
    def test_get_job_listings_success(self, automation):
        """Test successful job listings retrieval"""
        mock_driver = Mock()
        automation.driver = mock_driver
        
        # Mock job elements
        mock_job_element = Mock()
        mock_title_element = Mock()
        mock_company_element = Mock()
        
        mock_title_element.text = "Data Analyst"
        mock_company_element.text = "Test Company"
        
        mock_job_element.find_element.side_effect = [
            mock_title_element,  # Title element
            mock_company_element,  # Company element
            Mock()  # Easy Apply button (exists)
        ]
        
        mock_driver.find_elements.return_value = [mock_job_element]
        
        result = automation.get_job_listings(max_jobs=1)
        
        assert len(result) == 1
        assert result[0]['title'] == "Data Analyst"
        assert result[0]['company'] == "Test Company"
        assert result[0]['has_easy_apply'] is True
    
    def test_apply_to_job_without_driver(self, automation):
        """Test applying to job without driver"""
        job_info = {'title': 'Test Job', 'has_easy_apply': True}
        result = automation.apply_to_job(job_info)
        assert result is False
    
    def test_apply_to_job_no_easy_apply(self, automation):
        """Test applying to job without Easy Apply"""
        mock_driver = Mock()
        automation.driver = mock_driver
        
        job_info = {'title': 'Test Job', 'has_easy_apply': False}
        result = automation.apply_to_job(job_info)
        assert result is False
    
    def test_apply_to_job_daily_limit_reached(self, automation):
        """Test applying to job when daily limit is reached"""
        mock_driver = Mock()
        automation.driver = mock_driver
        automation.applications_today = 5  # Max limit
        
        job_info = {'title': 'Test Job', 'has_easy_apply': True}
        result = automation.apply_to_job(job_info)
        assert result is False
    
    def test_send_message_without_driver(self, automation):
        """Test sending message without driver"""
        result = automation.send_message("Test message")
        assert result is False
    
    @patch('linkedin_automation.WebDriverWait')
    def test_send_message_success(self, mock_wait_class, automation):
        """Test successful message sending"""
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
        
        result = automation.send_message("Test message")
        
        assert result is True
        mock_message_field.clear.assert_called_once()
        mock_message_field.send_keys.assert_called_with("Test message")
        mock_send_button.click.assert_called_once()
    
    def test_close_session(self, automation):
        """Test closing session"""
        mock_driver = Mock()
        automation.driver = mock_driver
        
        automation.close_session()
        
        mock_driver.quit.assert_called_once()
        assert automation.driver is None
    
    def test_get_application_stats(self, automation):
        """Test getting application statistics"""
        automation.applications_today = 3
        
        stats = automation.get_application_stats()
        
        assert stats['applications_today'] == 3
        assert stats['max_applications_per_day'] == 5
        assert stats['remaining_applications'] == 2
