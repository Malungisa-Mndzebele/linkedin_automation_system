"""
Quick Web Application Test Suite
Tests core functionality without complex dependencies
"""
import os
import sys

def test_file_structure():
    """Test that all required files exist"""
    print("🧪 Testing file structure...")
    
    required_files = [
        'app.py',
        'start_web_app.py',
        'requirements_web.txt',
        'WEB_APPLICATION_GUIDE.md',
        'templates/dashboard.html',
        'templates/config.html',
        'templates/monitor.html',
        'templates/jobs.html',
        'templates/logs.html',
        'static/js/dashboard.js',
        'static/js/config.js',
        'static/js/monitor.js',
        'static/css/dashboard.css'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"  ✅ {file}")
    
    if missing_files:
        print(f"  ❌ Missing files: {missing_files}")
        return False
    
    print("  ✅ All required files exist")
    return True

def test_imports():
    """Test that core modules can be imported"""
    print("🧪 Testing imports...")
    
    try:
        from config import LinkedInConfig, JobApplicationConfig
        print("  ✅ Config imports successful")
    except ImportError as e:
        print(f"  ❌ Config import failed: {e}")
        return False
    
    try:
        from comprehensive_logging import AutomationLogger
        print("  ✅ Comprehensive logging import successful")
    except ImportError as e:
        print(f"  ❌ Comprehensive logging import failed: {e}")
        return False
    
    try:
        from database import DatabaseManager
        print("  ✅ Database import successful")
    except ImportError as e:
        print(f"  ❌ Database import failed: {e}")
        return False
    
    try:
        from linkedin_automation import LinkedInAutomation
        print("  ✅ LinkedIn automation import successful")
    except ImportError as e:
        print(f"  ❌ LinkedIn automation import failed: {e}")
        return False
    
    try:
        import flask
        print(f"  ✅ Flask import successful: {flask.__version__}")
    except ImportError as e:
        print(f"  ❌ Flask import failed: {e}")
        return False
    
    return True

def test_config_creation():
    """Test configuration object creation"""
    print("🧪 Testing configuration creation...")
    
    try:
        from config import LinkedInConfig, JobApplicationConfig
        
        config = LinkedInConfig(
            email="test@example.com",
            password="testpassword",
            job_keywords=["Data Analyst"],
            easy_apply_only=True,
            max_applications_per_day=5
        )
        
        assert config.email == "test@example.com"
        assert config.job_keywords == ["Data Analyst"]
        assert config.easy_apply_only == True
        print("  ✅ LinkedInConfig creation successful")
        
        job_config = JobApplicationConfig()
        print("  ✅ JobApplicationConfig creation successful")
        
        return True
    except Exception as e:
        print(f"  ❌ Configuration creation failed: {e}")
        return False

def test_logging_system():
    """Test logging system"""
    print("🧪 Testing logging system...")
    
    try:
        from comprehensive_logging import AutomationLogger
        
        logger = AutomationLogger("INFO")
        logger.log_session_start()
        logger.log_user_configuration({"email": "test@example.com"})
        logger.log_job_search(["Data Analyst"], "San Francisco", True)
        logger.log_job_found(1, "Test Job", "Test Company", True)
        logger.log_job_application_attempt(1, "Test Job", "Test Company")
        logger.log_job_application_result(1, "Test Job", "Test Company", True)
        logger.log_session_end({"applications_sent": 1})
        
        print("  ✅ Logging system test successful")
        return True
    except Exception as e:
        print(f"  ❌ Logging system test failed: {e}")
        return False

def test_automation_class():
    """Test automation class"""
    print("🧪 Testing automation class...")
    
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
        assert 'applications_today' in stats
        assert 'max_applications_per_day' in stats
        assert 'remaining_applications' in stats
        
        print("  ✅ Automation class test successful")
        return True
    except Exception as e:
        print(f"  ❌ Automation class test failed: {e}")
        return False

def test_flask_app():
    """Test Flask application"""
    print("🧪 Testing Flask application...")
    
    try:
        from app import app
        
        # Test basic app configuration
        assert app.config['SECRET_KEY'] is not None
        assert app.config['TESTING'] == False  # Should be False by default
        
        print("  ✅ Flask app configuration test successful")
        
        # Test that routes are registered
        rules = [rule.rule for rule in app.url_map.iter_rules()]
        expected_routes = ['/', '/config', '/monitor', '/jobs', '/logs']
        
        for route in expected_routes:
            if route not in rules:
                print(f"  ❌ Missing route: {route}")
                return False
            print(f"  ✅ Route exists: {route}")
        
        return True
    except Exception as e:
        print(f"  ❌ Flask app test failed: {e}")
        return False

def run_quick_tests():
    """Run all quick tests"""
    print("=" * 60)
    print("LinkedIn Automation Web Application - Quick Tests")
    print("=" * 60)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("Configuration Creation", test_config_creation),
        ("Logging System", test_logging_system),
        ("Automation Class", test_automation_class),
        ("Flask Application", test_flask_app)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        try:
            if test_func():
                passed += 1
                print(f"✅ {test_name} PASSED")
            else:
                print(f"❌ {test_name} FAILED")
        except Exception as e:
            print(f"❌ {test_name} FAILED with exception: {e}")
    
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    print(f"Tests passed: {passed}/{total}")
    print(f"Success rate: {(passed/total*100):.1f}%")
    
    if passed == total:
        print("🎉 ALL TESTS PASSED! Web application is ready to use.")
        print("\n🚀 To start the web application:")
        print("   python start_web_app.py")
        print("   Then open: http://localhost:5000")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    return passed == total

if __name__ == "__main__":
    success = run_quick_tests()
    sys.exit(0 if success else 1)
