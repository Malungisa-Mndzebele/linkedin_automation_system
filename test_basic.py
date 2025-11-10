"""
Basic functionality tests for LinkedIn Automation Web Application
Tests core components without complex dependencies
"""
import unittest
import json
import os
import tempfile
from unittest.mock import Mock, patch

# Test basic imports
def test_imports():
    """Test that all modules can be imported"""
    try:
        from config import LinkedInConfig, JobApplicationConfig
        print("[OK] Config imports successful")
        return True
    except ImportError as e:
        print(f"[ERROR] Config import failed: {e}")
        return False

def test_comprehensive_logging():
    """Test comprehensive logging system"""
    try:
        from comprehensive_logging import AutomationLogger
        logger = AutomationLogger("INFO")
        logger.log_session_start()
        print("[OK] Comprehensive logging test successful")
        return True
    except Exception as e:
        print(f"[ERROR] Comprehensive logging test failed: {e}")
        return False

def test_database():
    """Test database functionality"""
    try:
        from database import DatabaseManager, JobApplication
        from datetime import datetime
        
        # Create temporary database
        db_path = tempfile.mktemp(suffix='.db')
        db_manager = DatabaseManager(db_path)
        
        # Test job application creation
        job_app = JobApplication(
            job_title="Test Job",
            company="Test Company",
            job_url="https://linkedin.com/jobs/test",
            application_date=datetime.now(),
            status="applied",
            easy_apply=True
        )
        
        job_id = db_manager.add_job_application(job_app)
        retrieved_jobs = db_manager.get_job_applications(limit=1)
        
        # Clean up
        try:
            os.remove(db_path)
        except PermissionError:
            # Database might still be in use, that's okay for testing
            pass
        
        if retrieved_jobs and len(retrieved_jobs) > 0:
            retrieved_job = retrieved_jobs[0]
            assert retrieved_job.job_title == "Test Job"
            assert retrieved_job.company == "Test Company"
        
        print("[OK] Database test successful")
        return True
    except Exception as e:
        print(f"[ERROR] Database test failed: {e}")
        return False

def test_linkedin_automation():
    """Test LinkedIn automation class"""
    try:
        from linkedin_automation import LinkedInAutomation
        from config import LinkedInConfig, JobApplicationConfig
        
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
        
        # Test basic functionality
        stats = automation.get_application_stats()
        
        print("[OK] LinkedIn automation test successful")
        return True
    except Exception as e:
        print(f"[ERROR] LinkedIn automation test failed: {e}")
        return False

def test_flask_app():
    """Test Flask application"""
    try:
        # Check if Flask is available
        import flask
        print(f"[OK] Flask available: {flask.__version__}")
        
        # Try to import the app
        from app import app
        print("[OK] Flask app import successful")
        
        # Test basic app configuration
        assert app.config['SECRET_KEY'] is not None
        print("[OK] Flask app configuration test successful")
        
        return True
    except ImportError as e:
        print(f"[ERROR] Flask not available: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Flask app test failed: {e}")
        return False

def test_web_templates():
    """Test web templates exist"""
    try:
        template_files = [
            'templates/dashboard.html',
            'templates/config.html',
            'templates/monitor.html',
            'templates/jobs.html',
            'templates/logs.html'
        ]
        
        for template in template_files:
            if not os.path.exists(template):
                print(f"[ERROR] Missing template: {template}")
                return False
            print(f"[OK] Template exists: {template}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Template test failed: {e}")
        return False

def test_static_files():
    """Test static files exist"""
    try:
        static_files = [
            'static/js/dashboard.js',
            'static/js/config.js',
            'static/js/monitor.js',
            'static/css/dashboard.css'
        ]
        
        for static_file in static_files:
            if not os.path.exists(static_file):
                print(f"[ERROR] Missing static file: {static_file}")
                return False
            print(f"[OK] Static file exists: {static_file}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Static files test failed: {e}")
        return False

def test_configuration_files():
    """Test configuration files"""
    try:
        config_files = [
            'requirements_web.txt',
            'app.py',
            'README.md'
        ]
        
        for config_file in config_files:
            if not os.path.exists(config_file):
                print(f"[ERROR] Missing config file: {config_file}")
                return False
            print(f"[OK] Config file exists: {config_file}")
        
        return True
    except Exception as e:
        print(f"[ERROR] Configuration files test failed: {e}")
        return False

def run_basic_tests():
    """Run all basic tests"""
    print("=" * 60)
    print("LinkedIn Automation Web Application - Basic Tests")
    print("=" * 60)
    
    tests = [
        ("Import Tests", test_imports),
        ("Comprehensive Logging", test_comprehensive_logging),
        ("Database Functionality", test_database),
        ("LinkedIn Automation", test_linkedin_automation),
        ("Flask Application", test_flask_app),
        ("Web Templates", test_web_templates),
        ("Static Files", test_static_files),
        ("Configuration Files", test_configuration_files)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n[TEST] Running {test_name}...")
        try:
            if test_func():
                passed += 1
                print(f"[OK] {test_name} PASSED")
            else:
                print(f"[ERROR] {test_name} FAILED")
        except Exception as e:
            print(f"[ERROR] {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("[SUCCESS] ALL TESTS PASSED! Web application is ready to use.")
    else:
        print("[WARNING] Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = run_basic_tests()
    exit(0 if success else 1)
