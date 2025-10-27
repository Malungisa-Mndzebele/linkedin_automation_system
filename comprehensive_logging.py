"""
Enhanced Logging System for LinkedIn Job Application Automation
Comprehensive logging to track every step performed during automation
"""
import logging
import sys
import os
from datetime import datetime
from typing import Optional, Dict, Any
import json


class AutomationLogger:
    """
    Comprehensive logging system for LinkedIn automation
    Tracks every step, decision, and result during the automation process
    """
    
    def __init__(self, log_level: str = "INFO"):
        """
        Initialize the logging system
        
        Args:
            log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        """
        self.log_level = getattr(logging, log_level.upper())
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.setup_loggers()
        
        # Automatically log session start
        self.log_session_start()
        
    def setup_loggers(self):
        """Setup all logging components"""
        
        # Create logs directory if it doesn't exist
        os.makedirs("logs", exist_ok=True)
        
        # 1. Main application logger
        self.main_logger = self._create_logger(
            name="linkedin_automation",
            filename=f"logs/automation_{self.session_id}.log",
            format_str="%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )
        
        # 2. Detailed actions logger
        self.actions_logger = self._create_logger(
            name="automation_actions",
            filename=f"logs/actions_{self.session_id}.log",
            format_str="%(asctime)s - ACTION - %(message)s"
        )
        
        # 3. Browser operations logger
        self.browser_logger = self._create_logger(
            name="browser_operations",
            filename=f"logs/browser_{self.session_id}.log",
            format_str="%(asctime)s - BROWSER - %(message)s"
        )
        
        # 4. Job processing logger
        self.job_logger = self._create_logger(
            name="job_processing",
            filename=f"logs/jobs_{self.session_id}.log",
            format_str="%(asctime)s - JOB - %(message)s"
        )
        
        # 5. Database operations logger
        self.db_logger = self._create_logger(
            name="database_operations",
            filename=f"logs/database_{self.session_id}.log",
            format_str="%(asctime)s - DATABASE - %(message)s"
        )
        
        # 6. AI operations logger
        self.ai_logger = self._create_logger(
            name="ai_operations",
            filename=f"logs/ai_{self.session_id}.log",
            format_str="%(asctime)s - AI - %(message)s"
        )
        
        # 7. Error logger
        self.error_logger = self._create_logger(
            name="errors",
            filename=f"logs/errors_{self.session_id}.log",
            format_str="%(asctime)s - ERROR - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s"
        )
        
        # 8. Performance logger
        self.perf_logger = self._create_logger(
            name="performance",
            filename=f"logs/performance_{self.session_id}.log",
            format_str="%(asctime)s - PERF - %(message)s"
        )
        
        # 9. Session summary logger
        self.session_logger = self._create_logger(
            name="session_summary",
            filename=f"logs/session_{self.session_id}.log",
            format_str="%(asctime)s - SESSION - %(message)s"
        )
        
        # Log session start
        self.log_session_start()
        
    def _create_logger(self, name: str, filename: str, format_str: str) -> logging.Logger:
        """Create a logger with file and console handlers"""
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        
        # Clear existing handlers
        logger.handlers.clear()
        
        # File handler
        file_handler = logging.FileHandler(filename, mode='a', encoding='utf-8')
        file_handler.setLevel(self.log_level)
        file_formatter = logging.Formatter(format_str)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)
        
        # Console handler (only for main logger)
        if name == "linkedin_automation":
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(logging.INFO)
            console_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)
        
        # Prevent duplicate logs
        logger.propagate = False
        
        return logger
        
    def log_session_start(self):
        """Log session start with comprehensive information"""
        self.session_logger.info("=" * 80)
        self.session_logger.info("LINKEDIN AUTOMATION SESSION STARTED")
        self.session_logger.info("=" * 80)
        self.session_logger.info(f"Session ID: {self.session_id}")
        self.session_logger.info(f"Start Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.session_logger.info(f"Python Version: {sys.version}")
        self.session_logger.info(f"Working Directory: {os.getcwd()}")
        self.session_logger.info("=" * 80)
        
    def log_session_end(self, stats: Dict[str, Any]):
        """Log session end with comprehensive statistics"""
        self.session_logger.info("=" * 80)
        self.session_logger.info("LINKEDIN AUTOMATION SESSION ENDED")
        self.session_logger.info("=" * 80)
        self.session_logger.info(f"End Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        self.session_logger.info(f"Session Duration: {stats.get('session_duration', 'Unknown')}")
        self.session_logger.info(f"Jobs Found: {stats.get('jobs_found', 0)}")
        self.session_logger.info(f"Applications Sent: {stats.get('applications_sent', 0)}")
        self.session_logger.info(f"Success Rate: {stats.get('success_rate', 0):.1f}%")
        self.session_logger.info(f"Errors Encountered: {stats.get('errors_count', 0)}")
        self.session_logger.info("=" * 80)
        
    def log_user_configuration(self, config: Dict[str, Any]):
        """Log user configuration details"""
        self.actions_logger.info("USER CONFIGURATION COLLECTED")
        self.actions_logger.info(f"Email: {config.get('email', 'Not provided')}")
        self.actions_logger.info(f"Job Keywords: {', '.join(config.get('job_keywords', []))}")
        self.actions_logger.info(f"Location: {config.get('location', 'Not specified')}")
        self.actions_logger.info(f"Max Applications/Day: {config.get('max_applications_per_day', 0)}")
        self.actions_logger.info(f"Easy Apply Only: {config.get('easy_apply_only', False)}")
        self.actions_logger.info(f"Experience Level: {config.get('experience_level', 'Not specified')}")
        self.actions_logger.info(f"Remote Preference: {config.get('remote_preference', False)}")
        
    def log_browser_start(self, headless: bool = False):
        """Log browser session start"""
        self.browser_logger.info("BROWSER SESSION STARTING")
        self.browser_logger.info(f"Headless Mode: {headless}")
        self.browser_logger.info(f"ChromeDriver: Auto-managed via webdriver-manager")
        
    def log_browser_end(self, success: bool = True):
        """Log browser session end"""
        status = "SUCCESS" if success else "FAILED"
        self.browser_logger.info(f"BROWSER SESSION ENDED - {status}")
        
    def log_browser_operation(self, operation: str, details: str = ""):
        """Log browser operations"""
        self.browser_logger.info(f"BROWSER OPERATION: {operation}")
        if details:
            self.browser_logger.info(f"Details: {details}")
        
    def log_login_attempt(self, email: str, success: bool = True):
        """Log LinkedIn login attempt"""
        status = "SUCCESS" if success else "FAILED"
        self.browser_logger.info(f"LINKEDIN LOGIN ATTEMPT - {status}")
        self.browser_logger.info(f"Email: {email}")
        if not success:
            self.error_logger.error("LinkedIn login failed")
            
    def log_job_search(self, keywords: list, location: str = "", easy_apply_only: bool = False):
        """Log job search initiation"""
        self.job_logger.info("JOB SEARCH INITIATED")
        self.job_logger.info(f"Keywords: {', '.join(keywords)}")
        self.job_logger.info(f"Location: {location if location else 'Any'}")
        self.job_logger.info(f"Easy Apply Only: {easy_apply_only}")
        
    def log_job_found(self, job_number: int, title: str, company: str, has_easy_apply: bool):
        """Log individual job found"""
        easy_apply_status = "YES" if has_easy_apply else "NO"
        self.job_logger.info(f"JOB {job_number}: {title} at {company} - Easy Apply: {easy_apply_status}")
        
    def log_job_application_attempt(self, job_number: int, title: str, company: str):
        """Log job application attempt"""
        self.actions_logger.info(f"APPLICATION ATTEMPT {job_number}: '{title}' at '{company}'")
        
    def log_job_application_result(self, job_number: int, title: str, company: str, success: bool, error: str = ""):
        """Log job application result"""
        status = "SUCCESS" if success else "FAILED"
        self.actions_logger.info(f"APPLICATION {job_number}: {status} - '{title}' at '{company}'")
        if not success and error:
            self.error_logger.error(f"Application failed: {error}")
            
    def log_database_operation(self, operation: str, table: str, details: str = ""):
        """Log database operations"""
        self.db_logger.info(f"DATABASE {operation.upper()}: {table}")
        if details:
            self.db_logger.info(f"Details: {details}")
            
    def log_ai_operation(self, operation: str, details: str = ""):
        """Log AI operations"""
        self.ai_logger.info(f"AI {operation.upper()}")
        if details:
            self.ai_logger.info(f"Details: {details}")
            
    def log_error(self, error_type: str, error_message: str, context: str = ""):
        """Log errors with context"""
        self.error_logger.error(f"{error_type.upper()}: {error_message}")
        if context:
            self.error_logger.error(f"Context: {context}")
            
    def log_performance(self, operation: str, duration: float, details: str = ""):
        """Log performance metrics"""
        self.perf_logger.info(f"{operation.upper()}: {duration:.2f}s")
        if details:
            self.perf_logger.info(f"Details: {details}")
            
    def log_step(self, step_number: int, step_name: str, status: str = "STARTED", details: str = ""):
        """Log automation steps"""
        self.actions_logger.info(f"STEP {step_number}: {step_name} - {status}")
        if details:
            self.actions_logger.info(f"Step Details: {details}")
            
    def log_decision(self, decision_type: str, decision: str, reasoning: str = ""):
        """Log automation decisions"""
        self.actions_logger.info(f"DECISION - {decision_type}: {decision}")
        if reasoning:
            self.actions_logger.info(f"Reasoning: {reasoning}")
            
    def log_statistics(self, stats: Dict[str, Any]):
        """Log session statistics"""
        self.session_logger.info("SESSION STATISTICS")
        for key, value in stats.items():
            self.session_logger.info(f"{key}: {value}")
            
    def create_session_report(self) -> Dict[str, Any]:
        """Create a comprehensive session report"""
        report = {
            "session_id": self.session_id,
            "start_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "log_files": {
                "main": f"logs/automation_{self.session_id}.log",
                "actions": f"logs/actions_{self.session_id}.log",
                "browser": f"logs/browser_{self.session_id}.log",
                "jobs": f"logs/jobs_{self.session_id}.log",
                "database": f"logs/database_{self.session_id}.log",
                "ai": f"logs/ai_{self.session_id}.log",
                "errors": f"logs/errors_{self.session_id}.log",
                "performance": f"logs/performance_{self.session_id}.log",
                "session": f"logs/session_{self.session_id}.log"
            }
        }
        
        # Save report to file
        with open(f"logs/session_report_{self.session_id}.json", 'w') as f:
            json.dump(report, f, indent=2)
            
        return report


def setup_comprehensive_logging(log_level: str = "INFO") -> AutomationLogger:
    """
    Setup comprehensive logging system
    
    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        
    Returns:
        AutomationLogger instance
    """
    return AutomationLogger(log_level)


# Example usage and integration
if __name__ == "__main__":
    # Example of how to use the comprehensive logging system
    logger = setup_comprehensive_logging("INFO")
    
    # Log session start
    logger.log_session_start()
    
    # Log user configuration
    config = {
        "email": "user@example.com",
        "job_keywords": ["Data Analyst", "Business Analyst"],
        "location": "San Francisco, CA",
        "max_applications_per_day": 10,
        "easy_apply_only": True,
        "experience_level": "mid",
        "remote_preference": True
    }
    logger.log_user_configuration(config)
    
    # Log browser operations
    logger.log_browser_start(headless=False)
    logger.log_login_attempt("user@example.com", success=True)
    
    # Log job search
    logger.log_job_search(["Data Analyst"], "San Francisco, CA", True)
    
    # Log job findings
    logger.log_job_found(1, "Senior Data Analyst", "Tech Corp", True)
    logger.log_job_found(2, "Data Scientist", "Startup Inc", False)
    
    # Log application attempts
    logger.log_job_application_attempt(1, "Senior Data Analyst", "Tech Corp")
    logger.log_job_application_result(1, "Senior Data Analyst", "Tech Corp", True)
    
    # Log session end
    stats = {
        "session_duration": "15 minutes",
        "jobs_found": 2,
        "applications_sent": 1,
        "success_rate": 100.0,
        "errors_count": 0
    }
    logger.log_session_end(stats)
    
    # Create session report
    report = logger.create_session_report()
    print("Session report created:", report["log_files"])
