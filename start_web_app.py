"""
LinkedIn Job Application Automation - Web Application Startup Script
Easy way to start the web application with all dependencies
"""
import os
import sys
import subprocess
import time
from pathlib import Path


def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True


def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing dependencies...")
    
    requirements_files = [
        "requirements_web.txt",
        "requirements.txt",
        "requirements_full.txt"
    ]
    
    for req_file in requirements_files:
        if os.path.exists(req_file):
            print(f"Installing from {req_file}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", req_file])
                print(f"✅ Dependencies from {req_file} installed successfully")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to install dependencies from {req_file}: {e}")
                return False
    
    return True


def check_directories():
    """Check and create necessary directories"""
    print("📁 Checking directories...")
    
    directories = [
        "templates",
        "static/css",
        "static/js",
        "logs"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"✅ Directory: {directory}")
    
    return True

def clear_logs():
    """Clear all log files on startup"""
    print("🧹 Clearing previous logs...")
    
    import shutil
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


def check_files():
    """Check if required files exist"""
    print("📄 Checking required files...")
    
    required_files = [
        "app.py",
        "templates/dashboard.html",
        "templates/config.html",
        "templates/monitor.html",
        "static/js/dashboard.js",
        "static/js/config.js",
        "static/js/monitor.js"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
        else:
            print(f"✅ File: {file}")
    
    if missing_files:
        print("❌ Missing files:")
        for file in missing_files:
            print(f"   - {file}")
        return False
    
    return True


def start_web_application():
    """Start the web application"""
    print("🚀 Starting LinkedIn Automation Web Application...")
    print("=" * 60)
    print("🌐 Web Application URLs:")
    print("   Dashboard:    http://localhost:5000")
    print("   Configuration: http://localhost:5000/config")
    print("   Live Monitor:  http://localhost:5000/monitor")
    print("   Job Management: http://localhost:5000/jobs")
    print("   System Logs:   http://localhost:5000/logs")
    print("=" * 60)
    print("📝 Instructions:")
    print("   1. Open your web browser")
    print("   2. Go to http://localhost:5000")
    print("   3. Configure your LinkedIn credentials")
    print("   4. Start the automation")
    print("=" * 60)
    print("⚠️  Note: Keep this terminal open while using the web application")
    print("   Press Ctrl+C to stop the application")
    print("=" * 60)
    
    try:
        # Start the Flask application
        subprocess.run([sys.executable, "app.py"])
    except KeyboardInterrupt:
        print("\n\n🛑 Web application stopped by user")
    except Exception as e:
        print(f"\n❌ Error starting web application: {e}")


def main():
    """Main startup function"""
    print("=" * 60)
    print("LinkedIn Job Application Automation - Web Application")
    print("=" * 60)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Failed to install dependencies")
        return 1
    
    # Clear logs
    clear_logs()
    
    # Check directories
    if not check_directories():
        print("❌ Failed to create directories")
        return 1
    
    # Check files
    if not check_files():
        print("❌ Missing required files")
        return 1
    
    print("\n✅ All checks passed!")
    print("🚀 Starting web application...")
    
    # Start the application
    start_web_application()
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
