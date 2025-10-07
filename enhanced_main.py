"""
Enhanced Main Entry Point for LinkedIn Job Application Automation
Full-featured version with web dashboard, AI matching, and advanced features
"""
import sys
import logging
import getpass
from typing import List, Dict, Any
from datetime import datetime

from config import LinkedInConfig, JobApplicationConfig
from enhanced_linkedin_automation import EnhancedLinkedInAutomation
from web_dashboard import WebDashboard, create_dashboard_templates
from scheduler import AutomationScheduler
from database import DatabaseManager


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
    
    print("\n5. Advanced Features:")
    ai_matching = input("Enable AI job matching? (y/n, default: y): ").strip().lower()
    enable_ai = ai_matching in ['y', 'yes', '']
    
    web_dashboard = input("Start web dashboard? (y/n, default: y): ").strip().lower()
    start_dashboard = web_dashboard in ['y', 'yes', '']
    
    print("\n6. Configuration Summary:")
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
    print(f"AI Matching: {'Enabled' if enable_ai else 'Disabled'}")
    print(f"Web Dashboard: {'Enabled' if start_dashboard else 'Disabled'}")
    print("=" * 40)
    
    confirm = input("\nProceed with these settings? (y/n): ").strip().lower()
    if confirm not in ['y', 'yes']:
        print("Configuration cancelled.")
        sys.exit(0)
    
    return (email, password, phone, keywords, location, max_apps, experience_years, 
            skills, education, easy_apply, remote, experience_level, company_size, 
            enable_ai, start_dashboard)


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


def start_web_dashboard(detailed_logger):
    """Start the web dashboard in a separate thread"""
    try:
        import threading
        
        def run_dashboard():
            create_dashboard_templates()
            dashboard = WebDashboard(debug=False)
            dashboard.run()
        
        dashboard_thread = threading.Thread(target=run_dashboard, daemon=True)
        dashboard_thread.start()
        
        detailed_logger.info("WEB_DASHBOARD_START - Web dashboard started on http://127.0.0.1:5000")
        print("\n[INFO] Web dashboard started at: http://127.0.0.1:5000")
        print("[INFO] You can monitor the automation in real-time through the dashboard")
        
    except Exception as e:
        detailed_logger.error(f"WEB_DASHBOARD_ERROR - Failed to start dashboard: {e}")
        print(f"[WARNING] Could not start web dashboard: {e}")


def main():
    """Enhanced main function"""
    detailed_logger = setup_enhanced_logging()
    
    try:
        detailed_logger.info("ENHANCED_AUTOMATION_START - Enhanced LinkedIn automation system started")
        
        # Get user input
        user_inputs = get_enhanced_user_input()
        (email, password, phone, keywords, location, max_apps, experience_years,
         skills, education, easy_apply, remote, experience_level, company_size,
         enable_ai, start_dashboard) = user_inputs
        
        detailed_logger.info(f"USER_CONFIG - Email: {email}, Keywords: {keywords}, Max Apps: {max_apps}")
        
        # Create configurations
        linkedin_config, job_config = create_enhanced_configs(
            email, password, phone, keywords, location, max_apps, experience_years,
            skills, education, easy_apply, remote, experience_level, company_size
        )
        
        # Start web dashboard if requested
        if start_dashboard:
            start_web_dashboard(detailed_logger)
            time.sleep(2)  # Give dashboard time to start
        
        # Initialize enhanced automation
        detailed_logger.info("AUTOMATION_INIT - Initializing enhanced LinkedIn automation")
        automation = EnhancedLinkedInAutomation(linkedin_config, job_config)
        
        # Configure AI matching
        if enable_ai:
            automation.min_match_score = 70.0  # Minimum AI match score
            automation.smart_filtering = True
            automation.resume_optimization = True
            detailed_logger.info("AI_FEATURES - AI job matching and optimization enabled")
        else:
            automation.smart_filtering = False
            automation.resume_optimization = False
            detailed_logger.info("AI_FEATURES - AI features disabled")
        
        print("\n[INFO] Starting enhanced LinkedIn automation...")
        print("[INFO] This may take several minutes depending on the number of jobs found")
        print("[INFO] Check the web dashboard for real-time progress (if enabled)")
        
        # Run enhanced automation
        result = automation.run_automation_enhanced()
        
        # Display results
        print("\n" + "=" * 60)
        print("ENHANCED AUTOMATION RESULTS")
        print("=" * 60)
        
        if result["success"]:
            print(f"[SUCCESS] Automation completed successfully!")
            print(f"Jobs Found: {result['jobs_found']}")
            print(f"Applications Sent: {result['applications_sent']}")
            print(f"Success Rate: {result['success_rate']:.1f}%")
            print(f"Session Duration: {result['session_duration']} minutes")
            
            detailed_logger.info(f"ENHANCED_AUTOMATION_SUCCESS - Jobs: {result['jobs_found']}, Applications: {result['applications_sent']}, Success Rate: {result['success_rate']:.1f}%")
        else:
            print(f"[ERROR] Automation failed: {result['error']}")
            detailed_logger.error(f"ENHANCED_AUTOMATION_FAILED - Error: {result['error']}")
        
        # Display additional statistics
        stats = automation.get_application_stats()
        if stats:
            print("\n[INFO] Additional Statistics:")
            db_stats = stats.get('database_stats', {})
            daily_progress = stats.get('daily_progress', {})
            
            print(f"Total Applications (30 days): {db_stats.get('total_applications', 0)}")
            print(f"Success Rate (30 days): {db_stats.get('success_rate', 0):.1f}%")
            print(f"Remaining Applications Today: {daily_progress.get('remaining_applications', 0)}")
        
        print("\n[INFO] Check the log files for detailed information:")
        print("- enhanced_automation.log (technical logs)")
        print("- enhanced_actions.log (action logs)")
        
        if start_dashboard:
            print("\n[INFO] Web dashboard is still running at: http://127.0.0.1:5000")
            print("[INFO] You can continue monitoring and controlling the system")
        
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
