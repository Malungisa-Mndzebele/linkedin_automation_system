"""
Comprehensive Unit Tests for LinkedIn Automation Web Application
Tests all components including Flask app, automation logic, and web interface
"""
import unittest
import json
import os
import tempfile
import threading
import time
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime

# Import Flask testing utilities
try:
    from flask import Flask
    from flask.testing import FlaskClient
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    print("Warning: Flask not available for testing")

# Import our modules
from config import LinkedInConfig, JobApplicationConfig
from linkedin_automation import LinkedInAutomation
from comprehensive_logging import AutomationLogger
from database import DatabaseManager


class TestConfig(unittest.TestCase):
    """Test configuration classes"""
    
    def test_linkedin_config_creation(self):
        """Test LinkedInConfig creation"""
        config = LinkedInConfig(
            email="test@example.com",
            password="testpassword",
            job_keywords=["Data Analyst"],
            easy_apply_only=True,
            max_applications_per_day=5
        )
        
        self.assertEqual(config.email, "test@example.com")
        self.assertEqual(config.password, "testpassword")
        self.assertEqual(config.job_keywords, ["Data Analyst"])
        self.assertTrue(config.easy_apply_only)
        self.assertEqual(config.max_applications_per_day, 5)
    
    def test_job_application_config_creation(self):
        """Test JobApplicationConfig creation"""
        config = JobApplicationConfig()
        
        # Test default values
        self.assertIsNotNone(config)
        self.assertTrue(hasattr(config, 'custom_resume_path'))
        self.assertTrue(hasattr(config, 'cover_letter_template'))


class TestComprehensiveLogging(unittest.TestCase):
    """Test comprehensive logging system"""
    
    def setUp(self):
        """Set up test environment"""
        self.logger = AutomationLogger("INFO")
    
    def test_logger_initialization(self):
        """Test logger initialization"""
        self.assertIsNotNone(self.logger)
        self.assertIsNotNone(self.logger.main_logger)
        self.assertIsNotNone(self.logger.actions_logger)
        self.assertIsNotNone(self.logger.browser_logger)
    
    def test_session_start_logging(self):
        """Test session start logging"""
        # This should not raise an exception
        self.logger.log_session_start()
        self.assertTrue(True)  # If we get here, logging worked
    
    def test_user_configuration_logging(self):
        """Test user configuration logging"""
        config = {
            "email": "test@example.com",
            "job_keywords": ["Data Analyst"],
            "max_applications_per_day": 5
        }
        
        # This should not raise an exception
        self.logger.log_user_configuration(config)
        self.assertTrue(True)
    
    def test_job_application_logging(self):
        """Test job application logging"""
        # This should not raise an exception
        self.logger.log_job_application_attempt(1, "Test Job", "Test Company")
        self.logger.log_job_application_result(1, "Test Job", "Test Company", True)
        self.assertTrue(True)


class TestDatabaseManager(unittest.TestCase):
    """Test database manager"""
    
    def setUp(self):
        """Set up test database"""
        self.db_path = tempfile.mktemp(suffix='.db')
        self.db_manager = DatabaseManager(self.db_path)
    
    def tearDown(self):
        """Clean up test database"""
        if os.path.exists(self.db_path):
            os.remove(self.db_path)
    
    def test_database_initialization(self):
        """Test database initialization"""
        self.assertIsNotNone(self.db_manager)
        self.assertTrue(os.path.exists(self.db_path))
    
    def test_job_application_crud(self):
        """Test job application CRUD operations"""
        from database import JobApplication
        
        # Create job application
        job_app = JobApplication(
            job_title="Test Job",
            company="Test Company",
            job_url="https://linkedin.com/jobs/test",
            application_date=datetime.now(),
            status="applied",
            easy_apply=True
        )
        
        # Add to database
        job_id = self.db_manager.add_job_application(job_app)
        self.assertIsNotNone(job_id)
        
        # Retrieve from database
        retrieved_job = self.db_manager.get_job_application(job_id)
        self.assertIsNotNone(retrieved_job)
        self.assertEqual(retrieved_job.job_title, "Test Job")
        self.assertEqual(retrieved_job.company, "Test Company")
    
    def test_job_search_crud(self):
        """Test job search CRUD operations"""
        from database import JobSearch
        
        # Create job search
        job_search = JobSearch(
            search_date=datetime.now(),
            keywords="Data Analyst",
            location="San Francisco",
            jobs_found=10,
            applications_sent=5,
            success_rate=50.0
        )
        
        # Add to database
        search_id = self.db_manager.add_job_search(job_search)
        self.assertIsNotNone(search_id)
        
        # Retrieve from database
        retrieved_search = self.db_manager.get_job_search(search_id)
        self.assertIsNotNone(retrieved_search)
        self.assertEqual(retrieved_search.keywords, "Data Analyst")


class TestLinkedInAutomation(unittest.TestCase):
    """Test LinkedIn automation class"""
    
    def setUp(self):
        """Set up test automation"""
        self.config = LinkedInConfig(
            email="test@example.com",
            password="testpassword",
            job_keywords=["Data Analyst"],
            easy_apply_only=True,
            max_applications_per_day=5,
            headless=True  # Use headless for testing
        )
        self.job_config = JobApplicationConfig()
        self.automation = LinkedInAutomation(self.config, self.job_config)
    
    def test_automation_initialization(self):
        """Test automation initialization"""
        self.assertIsNotNone(self.automation)
        self.assertEqual(self.automation.config.email, "test@example.com")
        self.assertEqual(self.automation.applications_today, 0)
    
    def test_logger_setup(self):
        """Test logger setup"""
        self.assertIsNotNone(self.automation.logger)
        self.assertIsNotNone(self.automation.comprehensive_logger)
    
    @patch('linkedin_automation.webdriver.Chrome')
    def test_driver_setup(self, mock_chrome):
        """Test driver setup with mocked Chrome"""
        mock_driver = Mock()
        mock_chrome.return_value = mock_driver
        
        driver = self.automation._setup_driver()
        
        self.assertIsNotNone(driver)
        mock_chrome.assert_called_once()
    
    def test_application_stats(self):
        """Test application statistics"""
        stats = self.automation.get_application_stats()
        
        self.assertIn('applications_today', stats)
        self.assertIn('max_applications_per_day', stats)
        self.assertIn('remaining_applications', stats)
        
        self.assertEqual(stats['applications_today'], 0)
        self.assertEqual(stats['max_applications_per_day'], 5)
        self.assertEqual(stats['remaining_applications'], 5)


class TestWebApplication(unittest.TestCase):
    """Test Flask web application"""
    
    def setUp(self):
        """Set up Flask test client"""
        if not FLASK_AVAILABLE:
            self.skipTest("Flask not available")
        
        # Import app after checking Flask availability
        from app import app
        self.app = app
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
    
    def test_home_page(self):
        """Test home page loads"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'LinkedIn Automation', response.data)
    
    def test_config_page(self):
        """Test configuration page loads"""
        response = self.client.get('/config')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Configuration', response.data)
    
    def test_monitor_page(self):
        """Test monitor page loads"""
        response = self.client.get('/monitor')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Live Monitor', response.data)
    
    def test_jobs_page(self):
        """Test jobs page loads"""
        response = self.client.get('/jobs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Job Applications', response.data)
    
    def test_logs_page(self):
        """Test logs page loads"""
        response = self.client.get('/logs')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'System Logs', response.data)
    
    def test_api_config_get(self):
        """Test API config GET endpoint"""
        response = self.client.get('/api/config')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIsInstance(data, dict)
    
    def test_api_config_post(self):
        """Test API config POST endpoint"""
        config_data = {
            "email": "test@example.com",
            "password": "testpassword",
            "job_keywords": ["Data Analyst"],
            "easy_apply_only": True,
            "max_applications_per_day": 5
        }
        
        response = self.client.post('/api/config',
                                   data=json.dumps(config_data),
                                   content_type='application/json')
        
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertTrue(data['success'])
    
    def test_api_automation_status(self):
        """Test API automation status endpoint"""
        response = self.client.get('/api/automation/status')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('is_running', data)
        self.assertIn('stats', data)
    
    def test_api_jobs(self):
        """Test API jobs endpoint"""
        response = self.client.get('/api/jobs')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('jobs', data)
        self.assertIsInstance(data['jobs'], list)
    
    def test_api_logs(self):
        """Test API logs endpoint"""
        response = self.client.get('/api/logs')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('logs', data)
        self.assertIsInstance(data['logs'], list)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system"""
    
    def setUp(self):
        """Set up integration test environment"""
        self.temp_dir = tempfile.mkdtemp()
        self.config_file = os.path.join(self.temp_dir, 'test_config.json')
        
        # Create test configuration
        test_config = {
            "email": "test@example.com",
            "password": "testpassword",
            "job_keywords": ["Data Analyst"],
            "easy_apply_only": True,
            "max_applications_per_day": 5
        }
        
        with open(self.config_file, 'w') as f:
            json.dump(test_config, f)
    
    def tearDown(self):
        """Clean up test environment"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)
    
    def test_config_loading(self):
        """Test configuration loading from file"""
        with open(self.config_file, 'r') as f:
            config = json.load(f)
        
        self.assertEqual(config['email'], "test@example.com")
        self.assertEqual(config['job_keywords'], ["Data Analyst"])
        self.assertTrue(config['easy_apply_only'])
    
    def test_automation_workflow(self):
        """Test complete automation workflow"""
        # Create configuration
        config = LinkedInConfig(
            email="test@example.com",
            password="testpassword",
            job_keywords=["Data Analyst"],
            easy_apply_only=True,
            max_applications_per_day=5,
            headless=True
        )
        
        job_config = JobApplicationConfig()
        automation = LinkedInAutomation(config, job_config)
        
        # Test initialization
        self.assertIsNotNone(automation)
        
        # Test statistics
        stats = automation.get_application_stats()
        self.assertIsInstance(stats, dict)
        self.assertIn('applications_today', stats)
    
    def test_logging_integration(self):
        """Test logging system integration"""
        logger = AutomationLogger("INFO")
        
        # Test various logging functions
        logger.log_session_start()
        logger.log_user_configuration({"email": "test@example.com"})
        logger.log_job_search(["Data Analyst"], "San Francisco", True)
        logger.log_job_found(1, "Test Job", "Test Company", True)
        logger.log_job_application_attempt(1, "Test Job", "Test Company")
        logger.log_job_application_result(1, "Test Job", "Test Company", True)
        logger.log_session_end({"applications_sent": 1})
        
        # If we get here without exceptions, logging works
        self.assertTrue(True)


class TestErrorHandling(unittest.TestCase):
    """Test error handling throughout the system"""
    
    def test_invalid_config_handling(self):
        """Test handling of invalid configuration"""
        with self.assertRaises(Exception):
            LinkedInConfig(
                email="",  # Invalid empty email
                password="testpassword",
                job_keywords=[]  # Invalid empty keywords
            )
    
    def test_database_error_handling(self):
        """Test database error handling"""
        # Try to create database with invalid path
        with self.assertRaises(Exception):
            DatabaseManager("/invalid/path/that/does/not/exist/test.db")
    
    def test_automation_error_handling(self):
        """Test automation error handling"""
        config = LinkedInConfig(
            email="test@example.com",
            password="testpassword",
            job_keywords=["Data Analyst"],
            easy_apply_only=True,
            max_applications_per_day=5,
            headless=True
        )
        
        job_config = JobApplicationConfig()
        automation = LinkedInAutomation(config, job_config)
        
        # Test error handling for invalid operations
        result = automation.start_session()
        # This might fail due to no Chrome driver, but shouldn't crash
        self.assertIsInstance(result, bool)


def run_comprehensive_tests():
    """Run all test suites"""
    print("=" * 60)
    print("LinkedIn Automation Web Application - Comprehensive Tests")
    print("=" * 60)
    
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestConfig,
        TestComprehensiveLogging,
        TestDatabaseManager,
        TestLinkedInAutomation,
        TestWebApplication,
        TestIntegration,
        TestErrorHandling
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_comprehensive_tests()
    exit(0 if success else 1)
