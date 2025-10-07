"""
Simplified Enhanced Main Entry Point for LinkedIn Job Application Automation
Works with available components without external dependencies
"""
import sys
import logging
import getpass
from typing import List, Dict, Any
from datetime import datetime

from config import LinkedInConfig, JobApplicationConfig
from linkedin_automation import LinkedInAutomation
from database import DatabaseManager
from simple_scheduler import SimpleScheduler


def setup_enhanced_logging():
    """Setup comprehensive logging for enhanced system"""
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('enhanced_automation.log', mode='a', encoding='utf-8')
        ]
    )
    
    # Detailed action logger
    detailed_logger = logging.getLogger('automation_actions')
    detailed_logger.setLevel(logging.INFO)
    detailed_handler = logging.FileHandler('enhanced_actions.log', mode='a', encoding='utf-8')
    detailed_formatter = logging.Formatter('%(asctime)s - ACTION - %(message)s')
    detailed_handler.setFormatter(detailed_formatter)
    detailed_logger.addHandler(detailed_handler)
    detailed_logger.propagate = False
    
    return detailed_logger


def get_enhanced_user_input() -> tuple:
    """Get comprehensive user input for enhanced automation"""
    print("=" * 60)
    print("LinkedIn Job Application Automation - Enhanced Version")
    print("=" * 60)
    print()
    
    # Basic credentials
    print("1. LinkedIn Credentials:")
    email = input("LinkedIn Email: ").strip()
    password = getpass.getpass("LinkedIn Password: ").strip()
    phone = input("Phone Number (optional): ").strip()
    
    print("\n2. Job Search Configuration:")
    keywords_input = input("Job Keywords (comma-separated): ").strip()
    keywords = [k.strip() for k in keywords_input.split(',') if k.strip()]
    
    location = input("Preferred Location (optional): ").strip()
    max_apps_input = input("Maximum applications per day (default: 10): ").strip()
    max_apps = int(max_apps_input) if max_apps_input.isdigit() else 10
    
    print("\n3. Experience & Skills:")
    experience_years_input = input("Years of experience (default: 0): ").strip()
    experience_years = int(experience_years_input) if experience_years_input.isdigit() else 0
    
    skills_input = input("Your skills (comma-separated): ").strip()
    skills = [s.strip() for s in skills_input.split(',') if s.strip()]
    
    education_input = input("Education (comma-separated): ").strip()
    education = [e.strip() for e in education_input.split(',') if e.strip()]
    
    print("\n4. Preferences:")
    easy_apply_only = input("Only apply to Easy Apply jobs? (y/n, default: y): ").strip().lower()
    easy_apply = easy_apply_only in ['y', 'yes', '']
    
    remote_preference = input("Prefer remote work? (y/n, default: n): ").strip().lower()
    remote = remote_preference in ['y', 'yes']
    
    experience_level = input("Experience level (entry/mid/senior/executive, default: mid): ").strip().lower()
    if experience_level not in ['entry', 'mid', 'senior', 'executive']:
        experience_level = 'mid'
    
    company_size = input("Preferred company size (startup/small/medium/large, default: medium): ").strip().lower()
    if company_size not in ['startup', 'small', 'medium', 'large']:
        company_size = 'medium'
    
    print("\n5. Configuration Summary:")
    print("=" * 40)
    print(f"Email: {email}")
    print(f"Job Keywords: {', '.join(keywords)}")
    print(f"Location: {location or 'Any'}")
    print(f"Max Applications/Day: {max_apps}")
    print(f"Experience: {experience_years} years ({experience_level})")
    print(f"Skills: {', '.join(skills[:3])}{'...' if len(skills) > 3 else ''}")
    print(f"Easy Apply Only: {'Yes' if easy_apply else 'No'}")
    print(f"Remote Preference: {'Yes' if remote else 'No'}")
    print(f"Company Size: {company_size}")
    print("=" * 40)
    
    confirm = input("\nProceed with these settings? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Configuration cancelled.")
        sys.exit(0)
    
    return (email, password, phone, keywords, location, max_apps, experience_years, 
            skills, education, easy_apply, remote, experience_level, company_size)


def create_enhanced_configs(email: str, password: str, phone: str, keywords: List[str], 
                          location: str, max_apps: int, experience_years: int, 
                          skills: List[str], education: List[str], easy_apply: bool,
                          remote: bool, experience_level: str, company_size: str) -> tuple:
    """Create enhanced configuration objects"""
    
    # LinkedIn configuration
    linkedin_config = LinkedInConfig(
        email=email,
        password=password,
        phone=phone
    )
    
    # Job application configuration
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
    
    return linkedin_config, job_config


def run_enhanced_automation(linkedin_config: LinkedInConfig, job_config: JobApplicationConfig, detailed_logger):
    """Run enhanced automation with database and scheduler integration"""
    try:
        # Initialize components
        automation = LinkedInAutomation(linkedin_config, job_config)
        db_manager = DatabaseManager()
        scheduler = SimpleScheduler()
        
        detailed_logger.info("ENHANCED_AUTOMATION_START - Enhanced automation session started")
        
        # Check if we can apply now
        can_apply, reason = scheduler.can_apply_now()
        if not can_apply:
            print(f"[INFO] Cannot start automation: {reason}")
            detailed_logger.info(f"AUTOMATION_BLOCKED - {reason}")
            return {"success": False, "error": reason}
        
        print(f"[INFO] Starting automation - {reason}")
        
        # Start session
        if not automation.start_session():
            return {"success": False, "error": "Failed to start session"}
        
        # Login
        if not automation.login():
            return {"success": False, "error": "Failed to login"}
        
        # Search jobs
        if not automation.search_jobs():
            return {"success": False, "error": "Failed to search jobs"}
        
        # Get and process jobs
        jobs = automation.get_job_listings()
        if not jobs:
            return {"success": False, "error": "No jobs found"}
        
        print(f"[INFO] Found {len(jobs)} jobs to process")
        
        # Apply to jobs
        successful_applications = 0
        for i, job in enumerate(jobs):
            print(f"[INFO] Processing job {i+1}/{len(jobs)}: {job.get('title', 'Unknown')} at {job.get('company', 'Unknown')}")
            
            # Check if we can still apply
            can_apply, reason = scheduler.can_apply_now()
            if not can_apply:
                print(f"[INFO] Stopping automation: {reason}")
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
        
        result = {
            "success": True,
            "jobs_found": len(jobs),
            "applications_sent": successful_applications,
            "success_rate": (successful_applications / len(jobs) * 100) if jobs else 0
        }
        
        print(f"[SUCCESS] Automation completed: {result}")
        detailed_logger.info(f"ENHANCED_AUTOMATION_SUCCESS - Jobs: {result['jobs_found']}, Applications: {result['applications_sent']}, Success Rate: {result['success_rate']:.1f}%")
        
        return result
        
    except Exception as e:
        print(f"[ERROR] Automation failed: {e}")
        detailed_logger.error(f"ENHANCED_AUTOMATION_ERROR - {e}")
        return {"success": False, "error": str(e)}
    
    finally:
        automation.close_session()


def main():
    """Enhanced main function"""
    detailed_logger = setup_enhanced_logging()
    
    try:
        detailed_logger.info("ENHANCED_AUTOMATION_START - Enhanced LinkedIn automation system started")
        
        # Get user input
        user_inputs = get_enhanced_user_input()
        (email, password, phone, keywords, location, max_apps, experience_years,
         skills, education, easy_apply, remote, experience_level, company_size) = user_inputs
        
        detailed_logger.info(f"USER_CONFIG - Email: {email}, Keywords: {keywords}, Max Apps: {max_apps}")
        
        # Create configurations
        linkedin_config, job_config = create_enhanced_configs(
            email, password, phone, keywords, location, max_apps, experience_years,
            skills, education, easy_apply, remote, experience_level, company_size
        )
        
        print("\n[INFO] Starting enhanced LinkedIn automation...")
        print("[INFO] This may take several minutes depending on the number of jobs found")
        
        # Run enhanced automation
        result = run_enhanced_automation(linkedin_config, job_config, detailed_logger)
        
        # Display results
        print("\n" + "=" * 60)
        print("ENHANCED AUTOMATION RESULTS")
        print("=" * 60)
        
        if result["success"]:
            print(f"[SUCCESS] Automation completed successfully!")
            print(f"Jobs Found: {result['jobs_found']}")
            print(f"Applications Sent: {result['applications_sent']}")
            print(f"Success Rate: {result['success_rate']:.1f}%")
            
            detailed_logger.info(f"ENHANCED_AUTOMATION_SUCCESS - Jobs: {result['jobs_found']}, Applications: {result['applications_sent']}, Success Rate: {result['success_rate']:.1f}%")
        else:
            print(f"[ERROR] Automation failed: {result['error']}")
            detailed_logger.error(f"ENHANCED_AUTOMATION_FAILED - Error: {result['error']}")
        
        # Display additional statistics
        try:
            db_manager = DatabaseManager()
            analytics = db_manager.get_analytics(30)
            scheduler = SimpleScheduler()
            daily_progress = scheduler.get_daily_progress()
            
            print("\n[INFO] Additional Statistics:")
            print(f"Total Applications (30 days): {analytics.get('total_applications', 0)}")
            print(f"Success Rate (30 days): {analytics.get('success_rate', 0):.1f}%")
            print(f"Remaining Applications Today: {daily_progress.get('remaining_applications', 0)}")
        except Exception as e:
            print(f"[WARNING] Could not load additional statistics: {e}")
        
        print("\n[INFO] Check the log files for detailed information:")
        print("- enhanced_automation.log (technical logs)")
        print("- enhanced_actions.log (action logs)")
        
    except KeyboardInterrupt:
        print("\n[INFO] Automation interrupted by user")
        detailed_logger.info("ENHANCED_AUTOMATION_INTERRUPTED - User interrupted automation")
        
    except Exception as e:
        print(f"\n[ERROR] Unexpected error: {e}")
        detailed_logger.error(f"ENHANCED_AUTOMATION_ERROR - Unexpected error: {e}")
        print("\n[INFO] Check the log files for more details")
    
    finally:
        print("\n[INFO] Enhanced LinkedIn automation session ended")
        detailed_logger.info("ENHANCED_AUTOMATION_END - Enhanced automation session ended")


if __name__ == "__main__":
    main()
