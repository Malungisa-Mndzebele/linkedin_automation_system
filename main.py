"""
Main entry point for LinkedIn Job Application Automation MVP
"""
import logging
import sys
import getpass
from typing import Optional

from linkedin_automation import LinkedInAutomation
from config import LinkedInConfig, JobApplicationConfig


def setup_logging():
    """Setup comprehensive logging configuration"""
    # Create a more detailed log format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(funcName)s:%(lineno)d - %(message)s'
    
    # Configure root logger
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('linkedin_automation.log', mode='a', encoding='utf-8')
        ]
    )
    
    # Create a separate detailed log file for automation actions
    detailed_logger = logging.getLogger('automation_actions')
    detailed_logger.setLevel(logging.INFO)
    
    # Create file handler for detailed actions
    detailed_handler = logging.FileHandler('automation_actions.log', mode='a', encoding='utf-8')
    detailed_handler.setLevel(logging.INFO)
    
    # Create formatter for detailed actions
    detailed_formatter = logging.Formatter(
        '%(asctime)s - ACTION - %(message)s'
    )
    detailed_handler.setFormatter(detailed_formatter)
    
    # Add handler to detailed logger
    detailed_logger.addHandler(detailed_handler)
    
    # Prevent duplicate logs
    detailed_logger.propagate = False
    
    return detailed_logger


def get_user_input():
    """Get user credentials and search preferences"""
    print("=" * 60)
    print("LinkedIn Job Application Automation MVP")
    print("=" * 60)
    print("This tool will help you automatically search and apply for jobs on LinkedIn.")
    print("You'll be prompted for your credentials and job search preferences.")
    print()
    
    # Get LinkedIn credentials
    print("Please enter your LinkedIn credentials:")
    email = input("LinkedIn Email: ").strip()
    password = getpass.getpass("LinkedIn Password: ").strip()
    
    if not email or not password:
        print("\n[ERROR] Email and password are required!")
        return None, None, None
    
    # Get job search preferences
    print("\nJob Search Configuration:")
    print("Enter job keywords (comma-separated, e.g., 'Data Analyst, Business Analyst'):")
    keywords_input = input("Job Keywords: ").strip()
    
    if not keywords_input:
        keywords = ["Data Analyst"]  # Default
        print("Using default: Data Analyst")
    else:
        keywords = [keyword.strip() for keyword in keywords_input.split(",")]
    
    # Get application preferences
    print("\nApplication Settings:")
    max_apps_input = input("Maximum applications per day (default: 10): ").strip()
    max_apps = 10  # Default
    if max_apps_input.isdigit():
        max_apps = int(max_apps_input)
    
    easy_apply_only = input("Only apply to Easy Apply jobs? (y/n, default: y): ").strip().lower()
    easy_apply = easy_apply_only != 'n'
    
    # Show configuration summary
    print("\n" + "=" * 60)
    print("Configuration Summary:")
    print("=" * 60)
    print(f"Email: {email}")
    print(f"Job Keywords: {', '.join(keywords)}")
    print(f"Max Applications/Day: {max_apps}")
    print(f"Easy Apply Only: {'Yes' if easy_apply else 'No'}")
    print("=" * 60)
    
    # Confirm before proceeding
    confirm = input("\nProceed with these settings? (y/n): ").strip().lower()
    if confirm != 'y':
        print("Operation cancelled.")
        return None, None, None, None, None
    
    return email, password, keywords, max_apps, easy_apply


def main():
    """Main function to run the LinkedIn automation"""
    detailed_logger = setup_logging()
    logger = logging.getLogger(__name__)
    
    # Log session start
    detailed_logger.info("=" * 80)
    detailed_logger.info("LINKEDIN AUTOMATION SESSION STARTED")
    detailed_logger.info("=" * 80)
    
    try:
        # Get user input
        detailed_logger.info("Starting user input collection")
        user_input = get_user_input()
        if user_input[0] is None:  # Check if email is None (error case)
            detailed_logger.info("User input collection failed - operation cancelled")
            return 1
            
        email, password, keywords, max_apps, easy_apply = user_input
        
        # Log user configuration (without password)
        detailed_logger.info(f"User configuration collected - Email: {email}")
        detailed_logger.info(f"Job keywords: {', '.join(keywords)}")
        detailed_logger.info(f"Max applications per day: {max_apps}")
        detailed_logger.info(f"Easy Apply only: {easy_apply}")
        
        # Create configuration
        logger.info("Creating configuration...")
        detailed_logger.info("Creating LinkedIn configuration object")
        config = LinkedInConfig(
            email=email,
            password=password,
            job_keywords=keywords,
            easy_apply_only=easy_apply,
            max_applications_per_day=max_apps,
            headless=False,  # Keep browser visible for user interaction
            implicit_wait=10,
            page_load_timeout=30
        )
        job_config = JobApplicationConfig()
        detailed_logger.info("Configuration created successfully")
        
        # Initialize automation
        logger.info("Initializing LinkedIn automation...")
        detailed_logger.info("Initializing LinkedInAutomation instance")
        automation = LinkedInAutomation(config, job_config)
        detailed_logger.info("LinkedInAutomation instance created")
        
        # Start session
        logger.info("Starting browser session...")
        detailed_logger.info("Attempting to start browser session")
        if not automation.start_session():
            logger.error("Failed to start browser session")
            detailed_logger.error("Browser session startup failed")
            return 1
        detailed_logger.info("Browser session started successfully")
        
        # Login to LinkedIn
        logger.info("Logging into LinkedIn...")
        detailed_logger.info(f"Attempting to login to LinkedIn with email: {email}")
        if not automation.login():
            logger.error("Failed to login to LinkedIn")
            detailed_logger.error("LinkedIn login failed")
            automation.close_session()
            return 1
        detailed_logger.info("LinkedIn login successful")
        
        # Search for jobs
        logger.info("Searching for jobs...")
        detailed_logger.info(f"Starting job search with keywords: {', '.join(keywords)}")
        if not automation.search_jobs():
            logger.error("Failed to search for jobs")
            detailed_logger.error("Job search failed")
            automation.close_session()
            return 1
        detailed_logger.info("Job search completed successfully")
        
        # Get job listings
        logger.info("Retrieving job listings...")
        detailed_logger.info("Fetching job listings from search results")
        jobs = automation.get_job_listings(max_jobs=10)
        
        if not jobs:
            logger.warning("No job listings found")
            detailed_logger.warning("No job listings found in search results")
            automation.close_session()
            return 0
        
        logger.info(f"Found {len(jobs)} job listings")
        detailed_logger.info(f"Retrieved {len(jobs)} job listings from LinkedIn")
        
        # Log all found jobs
        for i, job in enumerate(jobs, 1):
            detailed_logger.info(f"Job {i}: {job['title']} at {job['company']} - Easy Apply: {job['has_easy_apply']}")
        
        # Apply to jobs with Easy Apply
        easy_apply_jobs = [job for job in jobs if job['has_easy_apply']]
        logger.info(f"Found {len(easy_apply_jobs)} jobs with Easy Apply")
        detailed_logger.info(f"Identified {len(easy_apply_jobs)} jobs with Easy Apply functionality")
        
        applications_sent = 0
        detailed_logger.info("Starting job application process")
        
        for i, job in enumerate(easy_apply_jobs, 1):
            if applications_sent >= config.max_applications_per_day:
                logger.info("Daily application limit reached")
                detailed_logger.info(f"Daily application limit reached ({config.max_applications_per_day})")
                break
                
            logger.info(f"Applying to: {job['title']} at {job['company']}")
            detailed_logger.info(f"Application {i}: Attempting to apply to '{job['title']}' at '{job['company']}'")
            
            if automation.apply_to_job(job):
                applications_sent += 1
                logger.info(f"Successfully applied to {job['title']}")
                detailed_logger.info(f"Application {i}: SUCCESS - Applied to '{job['title']}' at '{job['company']}'")
            else:
                logger.warning(f"Failed to apply to {job['title']}")
                detailed_logger.warning(f"Application {i}: FAILED - Could not apply to '{job['title']}' at '{job['company']}'")
        
        detailed_logger.info(f"Job application process completed - {applications_sent} applications sent")
        
        # Display final statistics
        stats = automation.get_application_stats()
        print("\n" + "=" * 60)
        print("FINAL RESULTS")
        print("=" * 60)
        print(f"Applications sent today: {stats['applications_today']}")
        print(f"Remaining applications: {stats['remaining_applications']}")
        print("=" * 60)
        
        # Log final statistics
        logger.info("=== Application Statistics ===")
        logger.info(f"Applications sent today: {stats['applications_today']}")
        logger.info(f"Remaining applications: {stats['remaining_applications']}")
        
        detailed_logger.info("=== FINAL SESSION STATISTICS ===")
        detailed_logger.info(f"Total applications sent: {stats['applications_today']}")
        detailed_logger.info(f"Applications remaining today: {stats['remaining_applications']}")
        detailed_logger.info(f"Total jobs found: {len(jobs)}")
        detailed_logger.info(f"Jobs with Easy Apply: {len(easy_apply_jobs)}")
        detailed_logger.info(f"Success rate: {(applications_sent/len(easy_apply_jobs)*100):.1f}%" if easy_apply_jobs else "N/A")
        
        # Close session
        logger.info("Closing browser session...")
        detailed_logger.info("Closing browser session and cleaning up resources")
        automation.close_session()
        detailed_logger.info("Browser session closed successfully")
        
        # Log session completion
        detailed_logger.info("=" * 80)
        detailed_logger.info("LINKEDIN AUTOMATION SESSION COMPLETED SUCCESSFULLY")
        detailed_logger.info("=" * 80)
        
        print("\n*** LinkedIn automation completed successfully! ***")
        print("Check the log files for detailed information:")
        print("  - linkedin_automation.log (general logs)")
        print("  - automation_actions.log (detailed actions)")
        logger.info("LinkedIn automation completed successfully")
        return 0
        
    except KeyboardInterrupt:
        print("\n\n*** Automation interrupted by user ***")
        logger.info("Automation interrupted by user")
        detailed_logger.warning("Automation interrupted by user - session terminated")
        detailed_logger.info("=" * 80)
        detailed_logger.info("LINKEDIN AUTOMATION SESSION INTERRUPTED")
        detailed_logger.info("=" * 80)
        return 0
    except Exception as e:
        print(f"\n\n*** Unexpected error: {e} ***")
        print("Check the log files for more details:")
        print("  - linkedin_automation.log (general logs)")
        print("  - automation_actions.log (detailed actions)")
        logger.error(f"Unexpected error: {e}")
        detailed_logger.error(f"Unexpected error occurred: {str(e)}")
        detailed_logger.info("=" * 80)
        detailed_logger.info("LINKEDIN AUTOMATION SESSION FAILED")
        detailed_logger.info("=" * 80)
        return 1


if __name__ == "__main__":
    sys.exit(main())
