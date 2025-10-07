"""
Run LinkedIn automation with your specific configuration
"""
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


def main():
    """Run automation with your specific configuration"""
    detailed_logger = setup_logging()
    
    try:
        print("=" * 60)
        print("LinkedIn Job Application Automation - Your Configuration")
        print("=" * 60)
        print()
        
        # Your specific configuration
        email = "mndzebelemalungisa@gmail.com"
        password = input("Enter your LinkedIn password: ").strip()
        
        # Job search configuration
        keywords = ["analyst", "data", "data analyst"]
        location = "United States of America"
        max_apps = 10
        
        # Experience & skills
        experience_years = 4
        skills = ["data analysis"]
        education = ["BOA"]
        
        # Preferences
        easy_apply = True
        remote = False
        experience_level = "mid"
        company_size = "medium"
        
        print(f"\nConfiguration:")
        print(f"Email: {email}")
        print(f"Keywords: {', '.join(keywords)}")
        print(f"Location: {location}")
        print(f"Experience: {experience_years} years")
        print(f"Skills: {', '.join(skills)}")
        print(f"Easy Apply Only: {easy_apply}")
        print()
        
        # Create configurations
        linkedin_config = LinkedInConfig(
            email=email,
            password=password
        )
        
        job_config = JobApplicationConfig(
            keywords=keywords,
            location=location,
            max_applications_per_day=max_apps,
            easy_apply_only=easy_apply,
            experience_years=experience_years,
            skills=skills,
            education=education,
            remote_preference=remote,
            experience_level=experience_level,
            company_size=company_size
        )
        
        detailed_logger.info(f"USER_CONFIG - Email: {email}, Keywords: {keywords}, Max Apps: {max_apps}")
        
        # Initialize components
        automation = LinkedInAutomation(linkedin_config, job_config)
        db_manager = DatabaseManager()
        scheduler = SimpleScheduler()
        
        # Check if we can apply now
        can_apply, reason = scheduler.can_apply_now()
        print(f"[INFO] Scheduler check: {reason}")
        
        if not can_apply:
            print(f"[WARNING] Scheduler says: {reason}")
            print("[INFO] Proceeding anyway for testing purposes...")
        
        print("\n[INFO] Starting LinkedIn automation...")
        detailed_logger.info("AUTOMATION_START - Starting automation with your configuration")
        
        # Start session
        if not automation.start_session():
            print("[ERROR] Failed to start browser session")
            return
        
        # Login
        print("[INFO] Logging into LinkedIn...")
        if not automation.login():
            print("[ERROR] Failed to login to LinkedIn")
            return
        
        # Search jobs
        print("[INFO] Searching for jobs...")
        if not automation.search_jobs():
            print("[ERROR] Failed to search for jobs")
            return
        
        # Get job listings
        print("[INFO] Retrieving job listings...")
        jobs = automation.get_job_listings()
        
        if not jobs:
            print("[WARNING] No jobs found")
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
        
        # Additional stats
        try:
            analytics = db_manager.get_analytics(30)
            daily_progress = scheduler.get_daily_progress()
            
            print(f"\nAdditional Statistics:")
            print(f"Total Applications (30 days): {analytics.get('total_applications', 0)}")
            print(f"Remaining Applications Today: {daily_progress.get('remaining_applications', 0)}")
        except Exception as e:
            print(f"[WARNING] Could not load additional statistics: {e}")
        
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
