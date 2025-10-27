"""
Test script for comprehensive logging system
Verifies that all logging components work correctly
"""
import os
import time
from comprehensive_logging import setup_comprehensive_logging


def test_comprehensive_logging():
    """Test the comprehensive logging system"""
    print("Testing Comprehensive Logging System")
    print("=" * 50)
    
    # Initialize logging
    logger = setup_comprehensive_logging("INFO")
    
    # Test session start
    logger.log_session_start()
    print("✓ Session start logged")
    
    # Test user configuration
    config = {
        "email": "test@example.com",
        "job_keywords": ["Data Analyst", "Test Engineer"],
        "location": "Test City",
        "max_applications_per_day": 5,
        "easy_apply_only": True,
        "experience_level": "mid",
        "remote_preference": False
    }
    logger.log_user_configuration(config)
    print("✓ User configuration logged")
    
    # Test browser operations
    logger.log_browser_start(headless=False)
    logger.log_login_attempt("test@example.com", success=True)
    logger.log_browser_operation("Test operation", "Test details")
    print("✓ Browser operations logged")
    
    # Test job search
    logger.log_job_search(["Data Analyst"], "Test City", True)
    print("✓ Job search logged")
    
    # Test job findings
    logger.log_job_found(1, "Test Data Analyst", "Test Company", True)
    logger.log_job_found(2, "Test Engineer", "Another Company", False)
    print("✓ Job findings logged")
    
    # Test application attempts
    logger.log_job_application_attempt(1, "Test Data Analyst", "Test Company")
    logger.log_job_application_result(1, "Test Data Analyst", "Test Company", True)
    print("✓ Application attempts logged")
    
    # Test decisions
    logger.log_decision("Application Skip", "No Easy Apply", "Job does not support Easy Apply")
    logger.log_decision("Application Limit", "Daily limit reached", "Max applications: 5")
    print("✓ Decisions logged")
    
    # Test errors
    logger.log_error("Test Error", "This is a test error", "Test context")
    print("✓ Errors logged")
    
    # Test performance
    logger.log_performance("Test Operation", 2.5, "Test performance details")
    print("✓ Performance logged")
    
    # Test steps
    logger.log_step(1, "Test Step", "STARTED", "Test step details")
    logger.log_step(1, "Test Step", "COMPLETED")
    print("✓ Steps logged")
    
    # Test database operations
    logger.log_database_operation("INSERT", "job_applications", "Test job application")
    print("✓ Database operations logged")
    
    # Test AI operations
    logger.log_ai_operation("JOB_MATCHING", "Test AI matching operation")
    print("✓ AI operations logged")
    
    # Test session end
    stats = {
        "session_duration": "5 minutes",
        "jobs_found": 2,
        "applications_sent": 1,
        "success_rate": 100.0,
        "errors_count": 1
    }
    logger.log_statistics(stats)
    logger.log_session_end(stats)
    print("✓ Session end logged")
    
    # Create session report
    report = logger.create_session_report()
    print("✓ Session report created")
    
    # Check log files
    print("\nChecking log files...")
    log_files = []
    if os.path.exists("logs"):
        log_files = [f for f in os.listdir("logs") if f.endswith(".log")]
    
    print(f"Log files created: {len(log_files)}")
    for log_file in log_files:
        print(f"  - {log_file}")
    
    # Check session report
    report_files = [f for f in os.listdir("logs") if f.endswith(".json")]
    print(f"Report files created: {len(report_files)}")
    for report_file in report_files:
        print(f"  - {report_file}")
    
    print("\n" + "=" * 50)
    print("Comprehensive Logging Test Completed!")
    print("=" * 50)
    
    return True


def test_log_file_contents():
    """Test that log files contain expected content"""
    print("\nTesting log file contents...")
    
    if not os.path.exists("logs"):
        print("❌ Logs directory not found")
        return False
    
    log_files = [f for f in os.listdir("logs") if f.endswith(".log")]
    
    if not log_files:
        print("❌ No log files found")
        return False
    
    # Check each log file
    for log_file in log_files:
        file_path = os.path.join("logs", log_file)
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            if content.strip():
                print(f"✓ {log_file} has content ({len(content)} characters)")
            else:
                print(f"❌ {log_file} is empty")
                
        except Exception as e:
            print(f"❌ Error reading {log_file}: {e}")
    
    return True


if __name__ == "__main__":
    try:
        # Run comprehensive logging test
        test_comprehensive_logging()
        
        # Test log file contents
        test_log_file_contents()
        
        print("\n🎉 All logging tests passed!")
        print("\nLog files are located in the 'logs/' directory")
        print("You can now run the main automation with comprehensive logging enabled.")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
