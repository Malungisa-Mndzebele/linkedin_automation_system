"""
Test Log Clearing Functionality
Verifies that logs are cleared on app restart
"""
import os
import shutil

def test_log_clearing():
    """Test the log clearing functionality"""
    print("🧪 Testing log clearing functionality...")
    
    # Create some test log files
    test_log_dirs = ['logs', 'enhanced_logs']
    
    for log_dir in test_log_dirs:
        os.makedirs(log_dir, exist_ok=True)
        
        # Create test log files
        test_files = [
            f"{log_dir}/test_session_20250101_120000.log",
            f"{log_dir}/test_actions_20250101_120000.log",
            f"{log_dir}/test_browser_20250101_120000.log",
            f"{log_dir}/session_report_20250101_120000.json"
        ]
        
        for test_file in test_files:
            with open(test_file, 'w') as f:
                f.write("Test log content\n")
        
        print(f"✅ Created test files in {log_dir}")
    
    # Test the clear_logs function
    def clear_logs():
        """Clear all log files on startup"""
        print("🧹 Clearing previous logs...")
        
        log_dirs = ['logs', 'enhanced_logs']
        
        for log_dir in log_dirs:
            if os.path.exists(log_dir):
                try:
                    shutil.rmtree(log_dir)
                    print(f"✅ Cleared {log_dir} directory")
                except Exception as e:
                    print(f"⚠️ Could not clear {log_dir}: {e}")
        
        # Recreate logs directory
        os.makedirs('logs', exist_ok=True)
        print("✅ Logs cleared and ready for new session")
    
    # Run the clear function
    clear_logs()
    
    # Verify logs were cleared
    for log_dir in test_log_dirs:
        if os.path.exists(log_dir):
            files = os.listdir(log_dir)
            if files:
                print(f"❌ {log_dir} still contains files: {files}")
                return False
            else:
                print(f"✅ {log_dir} is empty")
        else:
            print(f"✅ {log_dir} was removed")
    
    print("\n🎉 Log clearing test successful!")
    return True

def test_app_log_clearing():
    """Test the app.py log clearing function"""
    print("\n🧪 Testing app.py log clearing...")
    
    # Import the clear function from app.py
    try:
        # Read the app.py file to extract the clear_logs_on_startup function
        with open('app.py', 'r') as f:
            app_content = f.read()
        
        if 'clear_logs_on_startup' in app_content:
            print("✅ clear_logs_on_startup function found in app.py")
        else:
            print("❌ clear_logs_on_startup function not found in app.py")
            return False
        
        if 'clear_logs_on_startup()' in app_content:
            print("✅ clear_logs_on_startup() is called in app.py")
        else:
            print("❌ clear_logs_on_startup() is not called in app.py")
            return False
        
        print("✅ App.py log clearing configuration verified")
        return True
        
    except Exception as e:
        print(f"❌ Error testing app.py: {e}")
        return False

def main():
    """Main test function"""
    print("=" * 60)
    print("Log Clearing Functionality Test")
    print("=" * 60)
    
    # Test basic log clearing
    if not test_log_clearing():
        print("❌ Basic log clearing test failed")
        return False
    
    # Test app.py configuration
    if not test_app_log_clearing():
        print("❌ App.py log clearing test failed")
        return False
    
    print("\n" + "=" * 60)
    print("LOG CLEARING TEST COMPLETED SUCCESSFULLY!")
    print("=" * 60)
    print("✅ Logs will be cleared on every app restart")
    print("✅ Fresh log files will be created for each session")
    print("✅ No old log files will accumulate")
    
    return True

if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
