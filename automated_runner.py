"""
Automated LinkedIn Job Application Runner
Uses configuration file instead of interactive input
"""
import json
import sys
import logging
from datetime import datetime

from config import LinkedInConfig, JobApplicationConfig
from linkedin_automation import LinkedInAutomation
from database import DatabaseManager
from simple_scheduler import SimpleScheduler


def setup_logging():
    """Setup logging"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('enhanced_automation.log', mode='a', encoding='utf-8')
        ]
    )
    
    detailed_logger = logging.getLogger('automation_actions')
    detailed_logger.setLevel(logging.INFO)
    detailed_handler = logging.FileHandler('enhanced_actions.log', mode='a', encoding='utf-8')
    detailed_formatter = logging.Formatter('%(asctime)s - ACTION - %(message)s')
    detailed_handler.setFormatter(detailed_formatter)
    detailed_logger.addHandler(detailed_handler)
    detailed_logger.propagate = False
    
    return detailed_logger


def load_config():
    """Load configuration from file"""
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
        return config
    except FileNotFoundError:
        print("[ERROR] config.json not found. Please create it first.")
        return None
    except Exception as e:
        print(f"[ERROR] Failed to load config: {e}")
        return None


def main():
    """Run automation using configuration file"""
    detailed_logger = setup_logging()
    
    try:
        print("=" * 60)
        print("LinkedIn Job Application Automation - Automated Mode")
        print("=" * 60)
        print()
        
        # Load configuration
        config = load_config()
        if not config:
            return
        
        # Check if password is set
        if config.get('linkedin_password') == 'YOUR_PASSWORD_HERE':
            print("[ERROR] Please update the password in config.json")
            print("Edit config.json and replace 'YOUR_PASSWORD_HERE' with your actual password")
            return
        
        print(f"Configuration loaded:")
        print(f"Email: {config.get('linkedin_email')}")
        print(f"Keywords: {', '.join(config.get('job_keywords', []))}")
        print(f"Location: {config.get('preferred_location')}")
        print(f"Experience: {config.get('experience_years')} years")
        print()
        
        # Create configurations
        linkedin_config = LinkedInConfig(
            email=config.get('linkedin_email'),
            password=config.get('linkedin_password')
        )
        
        job_config = JobApplicationConfig(
            keywords=config.get('job_keywords', []),
            location=config.get('preferred_location'),
            max_applications_per_day=config.get('max_applications_per_day', 10),
            easy_apply_only=config.get('easy_apply_only', True),
            experience_years=config.get('experience_years', 0),
            skills=config.get('skills', []),
            education=config.get('education', []),
            remote_preference=config.get('remote_preference', False),
            experience_level=config.get('experience_level', 'mid'),
            company_size=config.get('company_size', 'medium')
        )
        
        detailed_logger.info(f"USER_CONFIG - Email: {config.get('linkedin_email')}, Keywords: {config.get('job_keywords')}")
        
        # Initialize components
        automation = LinkedInAutomation(linkedin_config, job_config)
        db_manager = DatabaseManager()
        scheduler = SimpleScheduler()
        
        # Check if we can apply now
        can_apply, reason = scheduler.can_apply_now()
        print(f"[INFO] Scheduler check: {reason}")
        
        print("\n[INFO] Starting LinkedIn automation...")
        detailed_logger.info("AUTOMATION_START - Starting automated automation")
        
        # Start session
        if not automation.start_session():
            print("[ERROR] Failed to start browser session")
            detailed_logger.error("AUTOMATION_ERROR - Failed to start browser session")
            return
        
        # Login
        print("[INFO] Logging into LinkedIn...")
        if not automation.login():
            print("[ERROR] Failed to login to LinkedIn")
            detailed_logger.error("AUTOMATION_ERROR - Failed to login to LinkedIn")
            return
        
        # Search jobs
        print("[INFO] Searching for jobs...")
        if not automation.search_jobs():
            print("[ERROR] Failed to search for jobs")
            detailed_logger.error("AUTOMATION_ERROR - Failed to search for jobs")
            return
        
        # Get job listings
        print("[INFO] Retrieving job listings...")
        jobs = automation.get_job_listings()
        
        if not jobs:
            print("[WARNING] No jobs found")
            detailed_logger.warning("AUTOMATION_WARNING - No jobs found")
            return
        
        print(f"[SUCCESS] Found {len(jobs)} jobs")
        
        # Apply to jobs
        successful_applications = 0
        for i, job in enumerate(jobs[:5]):  # Limit to first 5 jobs for testing
            print(f"\n[INFO] Processing job {i+1}/5: {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')}")
            
            # Check scheduler
            can_apply, reason = scheduler.can_apply_now()
            if not can_apply and scheduler.daily_stats["applications_sent"] >= scheduler.config["daily_application_limit"]:
                print(f"[INFO] Daily limit reached: {reason}")
                break
            
            # Apply to job
            if automation.apply_to_job(job):
                successful_applications += 1
                scheduler.record_application()
                
                # Record in database
                from database import JobApplication
                application = JobApplication(
                    job_title=job.get('title', ''),
                    company=job.get('company', ''),
                    job_url=job.get('job_url', ''),
                    application_date=datetime.now(),
                    status='applied',
                    easy_apply=job.get('easy_apply', False),
                    location=job.get('location', ''),
                    job_description=job.get('description', '')
                )
                
                app_id = db_manager.add_job_application(application)
                print(f"[SUCCESS] Applied to job (ID: {app_id})")
                detailed_logger.info(f"APPLICATION_SUCCESS - Applied to {job.get('title')} at {job.get('company')} (ID: {app_id})")
            else:
                print(f"[WARNING] Failed to apply to job: {job.get('title')}")
                detailed_logger.warning(f"APPLICATION_FAILED - Failed to apply to {job.get('title')} at {job.get('company')}")
        
        # Results
        print("\n" + "=" * 60)
        print("AUTOMATION RESULTS")
        print("=" * 60)
        print(f"Jobs Found: {len(jobs)}")
        print(f"Applications Sent: {successful_applications}")
        print(f"Success Rate: {(successful_applications / len(jobs) * 100):.1f}%")
        
        detailed_logger.info(f"AUTOMATION_SUCCESS - Jobs: {len(jobs)}, Applications: {successful_applications}")
        
    except KeyboardInterrupt:
        print("\n[INFO] Automation interrupted by user")
        detailed_logger.info("AUTOMATION_INTERRUPTED - User interrupted")
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        detailed_logger.error(f"AUTOMATION_ERROR - {e}")
        
    finally:
        try:
            automation.close_session()
        except:
            pass
        print("\n[INFO] Automation session ended")
        detailed_logger.info("AUTOMATION_END - Session ended")


if __name__ == "__main__":
    main()
