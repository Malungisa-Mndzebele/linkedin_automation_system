"""
Enhanced LinkedIn Job Application Automation System
Full-featured version with AI matching, database integration, and advanced features
"""
import time
import random
import logging
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

from config import LinkedInConfig, JobApplicationConfig
from database import DatabaseManager, JobApplication, JobSearch
from ai_job_matcher import AIJobMatcher, UserProfile, JobMatch
from scheduler import AutomationScheduler


class EnhancedLinkedInAutomation:
    """Enhanced LinkedIn automation with full features"""
    
    def __init__(self, config: LinkedInConfig, job_config: JobApplicationConfig):
        self.config = config
        self.job_config = job_config
        self.logger = logging.getLogger(__name__)
        self.detailed_logger = logging.getLogger('automation_actions')
        
        # Initialize components
        self.db_manager = DatabaseManager()
        self.ai_matcher = AIJobMatcher()
        self.scheduler = AutomationScheduler()
        
        # WebDriver components
        self.driver = None
        self.wait = None
        
        # Session tracking
        self.session_start_time = None
        self.applications_sent = 0
        self.jobs_processed = 0
        self.current_search_session = None
        
        # AI matching
        self.user_profile = self._create_user_profile()
        self.min_match_score = 70.0  # Minimum AI match score to apply
        
        # Advanced features
        self.smart_filtering = True
        self.auto_messaging = False
        self.resume_optimization = True
        
        self.logger.info("Enhanced LinkedIn automation initialized")
    
    def _create_user_profile(self) -> UserProfile:
        """Create user profile for AI matching"""
        return UserProfile(
            skills=self.job_config.skills or [],
            experience_years=self.job_config.experience_years or 0,
            education=self.job_config.education or [],
            certifications=self.job_config.certifications or [],
            preferred_industries=self.job_config.preferred_industries or [],
            preferred_locations=self.job_config.preferred_locations or [],
            salary_expectation=self.job_config.salary_expectation,
            remote_preference=self.job_config.remote_preference or False,
            company_size_preference=self.job_config.company_size_preference or "medium"
        )
    
    def start_session(self) -> bool:
        """Start browser session with enhanced features"""
        try:
            self.logger.info("Starting enhanced browser session...")
            self.detailed_logger.info("SESSION_START - Enhanced automation session initiated")
            
            self.driver = self._setup_enhanced_driver()
            self.wait = WebDriverWait(self.driver, 20)
            
            # Set up session tracking
            self.session_start_time = datetime.now()
            self.applications_sent = 0
            self.jobs_processed = 0
            
            # Start new search session
            self.current_search_session = JobSearch(
                search_date=self.session_start_time,
                keywords=', '.join(self.job_config.keywords or []),
                location=self.job_config.location or ""
            )
            
            self.logger.info("Enhanced browser session started successfully")
            self.detailed_logger.info("SESSION_START - Browser session established with enhanced features")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start enhanced session: {e}")
            self.detailed_logger.error(f"SESSION_ERROR - Failed to start: {e}")
            return False
    
    def _setup_enhanced_driver(self) -> webdriver.Chrome:
        """Setup Chrome driver with enhanced options"""
        chrome_options = Options()
        
        # Enhanced stealth options
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--disable-extensions")
        chrome_options.add_argument("--disable-plugins")
        chrome_options.add_argument("--disable-images")  # Faster loading
        chrome_options.add_argument("--disable-javascript")  # Optional: for faster loading
        
        # User agent
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        
        # Unique user data directory
        import tempfile
        import os
        temp_dir = tempfile.mkdtemp()
        user_data_dir = os.path.join(temp_dir, "chrome_user_data")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        
        # Performance options
        chrome_options.add_argument("--memory-pressure-off")
        chrome_options.add_argument("--max_old_space_size=4096")
        
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        
        # Enhanced driver settings
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.implicitly_wait(10)
        driver.set_page_load_timeout(30)
        
        return driver
    
    def login(self) -> bool:
        """Enhanced login with better error handling"""
        try:
            self.logger.info("Starting enhanced LinkedIn login process")
            self.detailed_logger.info("LOGIN_START - Enhanced login process initiated")
            
            self.driver.get("https://www.linkedin.com/login")
            time.sleep(random.uniform(2, 4))
            
            # Enhanced login with retry logic
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    # Email field
                    email_field = self.wait.until(
                        EC.presence_of_element_located((By.ID, "username"))
                    )
                    email_field.clear()
                    email_field.send_keys(self.config.email)
                    time.sleep(random.uniform(0.5, 1.5))
                    
                    # Password field
                    password_field = self.driver.find_element(By.ID, "password")
                    password_field.clear()
                    password_field.send_keys(self.config.password)
                    time.sleep(random.uniform(0.5, 1.5))
                    
                    # Submit
                    login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
                    login_button.click()
                    
                    # Wait for login completion
                    time.sleep(random.uniform(3, 5))
                    
                    # Check for successful login
                    if self._is_logged_in():
                        self.logger.info("Successfully logged into LinkedIn with enhanced features")
                        self.detailed_logger.info("LOGIN_SUCCESS - Enhanced login completed successfully")
                        return True
                    else:
                        self.logger.warning(f"Login attempt {attempt + 1} failed, retrying...")
                        
                except Exception as e:
                    self.logger.warning(f"Login attempt {attempt + 1} failed: {e}")
                    if attempt < max_retries - 1:
                        time.sleep(random.uniform(2, 4))
            
            self.logger.error("All login attempts failed")
            self.detailed_logger.error("LOGIN_FAILED - All enhanced login attempts failed")
            return False
            
        except Exception as e:
            self.logger.error(f"Enhanced login failed: {e}")
            self.detailed_logger.error(f"LOGIN_ERROR - Enhanced login failed: {e}")
            return False
    
    def _is_logged_in(self) -> bool:
        """Check if user is logged in with enhanced detection"""
        try:
            # Multiple indicators of successful login
            indicators = [
                "//div[contains(@class, 'global-nav')]",
                "//div[contains(@class, 'feed-identity-module')]",
                "//div[contains(@class, 'profile-photo')]",
                "//a[contains(@href, '/in/')]",
                "//button[contains(@aria-label, 'View profile')]"
            ]
            
            for indicator in indicators:
                try:
                    element = self.driver.find_element(By.XPATH, indicator)
                    if element:
                        return True
                except NoSuchElementException:
                    continue
            
            # Check URL
            current_url = self.driver.current_url
            if "feed" in current_url or "in/" in current_url:
                return True
            
            return False
            
        except Exception as e:
            self.logger.warning(f"Error checking login status: {e}")
            return False
    
    def search_jobs_enhanced(self, keywords: Optional[List[str]] = None) -> bool:
        """Enhanced job search with AI filtering"""
        try:
            search_keywords = keywords or self.job_config.keywords or ["Data Analyst"]
            search_term = " ".join(search_keywords)
            
            self.logger.info(f"Starting enhanced job search with keywords: {search_term}")
            self.detailed_logger.info(f"SEARCH_START - Enhanced search initiated for: {search_term}")
            
            # Build enhanced search URL
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={search_term.replace(' ', '%20')}"
            
            # Add filters
            if self.job_config.easy_apply_only:
                search_url += "&f_LF=f_AL"  # Easy Apply filter
            
            if self.job_config.location:
                search_url += f"&location={self.job_config.location.replace(' ', '%20')}"
            
            # Experience level filter
            if self.job_config.experience_level:
                exp_mapping = {
                    "entry": "1",
                    "mid": "2", 
                    "senior": "3",
                    "executive": "4"
                }
                if self.job_config.experience_level in exp_mapping:
                    search_url += f"&f_E={exp_mapping[self.job_config.experience_level]}"
            
            # Company size filter
            if self.job_config.company_size:
                size_mapping = {
                    "startup": "1",
                    "small": "2",
                    "medium": "3", 
                    "large": "4"
                }
                if self.job_config.company_size in size_mapping:
                    search_url += f"&f_C={size_mapping[self.job_config.company_size]}"
            
            self.driver.get(search_url)
            time.sleep(random.uniform(3, 5))
            
            # Wait for job results to load
            try:
                self.wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "[data-test-id='job-card']"))
                )
            except TimeoutException:
                self.logger.warning("Job search results may not have loaded properly")
                self.detailed_logger.warning("SEARCH_WARNING - Job results may not have loaded properly")
            
            self.logger.info("Enhanced job search completed successfully")
            self.detailed_logger.info("SEARCH_SUCCESS - Enhanced job search completed")
            return True
            
        except Exception as e:
            self.logger.error(f"Enhanced job search failed: {e}")
            self.detailed_logger.error(f"SEARCH_ERROR - Enhanced job search failed: {e}")
            return False
    
    def get_job_listings_enhanced(self) -> List[Dict[str, Any]]:
        """Get job listings with AI analysis"""
        try:
            self.logger.info("Retrieving job listings with AI analysis...")
            self.detailed_logger.info("JOB_ANALYSIS_START - Starting AI-powered job analysis")
            
            # Enhanced job selectors
            job_selectors = [
                "//div[contains(@class, 'job-card-container')]",
                "//div[contains(@class, 'jobs-search-results-list')]//li",
                "//div[contains(@data-test-id, 'job-card')]",
                "//article[contains(@class, 'job-card')]",
                "//div[contains(@class, 'base-card')]"
            ]
            
            job_elements = []
            for selector in job_selectors:
                try:
                    elements = self.driver.find_elements(By.XPATH, selector)
                    if elements:
                        job_elements = elements
                        self.logger.info(f"Found {len(elements)} job elements using selector: {selector}")
                        break
                except Exception as e:
                    self.logger.debug(f"Selector {selector} failed: {e}")
                    continue
            
            if not job_elements:
                self.logger.warning("No job elements found with any selector")
                self.detailed_logger.warning("JOB_ANALYSIS_WARNING - No job elements found")
                return []
            
            jobs = []
            for i, job_element in enumerate(job_elements[:20]):  # Limit to first 20 jobs
                try:
                    job_data = self._extract_job_data_enhanced(job_element, i + 1)
                    if job_data:
                        # AI analysis
                        if self.smart_filtering:
                            job_match = self.ai_matcher.match_job(
                                self.user_profile,
                                job_data['title'],
                                job_data.get('description', ''),
                                job_data['company']
                            )
                            
                            job_data['ai_match'] = {
                                'score': job_match.match_score,
                                'reasons': job_match.reasons,
                                'missing_skills': job_match.missing_skills,
                                'recommendations': job_match.recommended_actions
                            }
                            
                            # Only include jobs above minimum match score
                            if job_match.match_score >= self.min_match_score:
                                jobs.append(job_data)
                                self.logger.info(f"Job {i+1} passed AI filter (score: {job_match.match_score:.1f})")
                            else:
                                self.logger.info(f"Job {i+1} filtered out by AI (score: {job_match.match_score:.1f})")
                        else:
                            jobs.append(job_data)
                        
                        self.jobs_processed += 1
                        
                except Exception as e:
                    self.logger.warning(f"Could not process job {i+1}: {e}")
                    continue
            
            self.logger.info(f"Retrieved {len(jobs)} jobs after AI filtering")
            self.detailed_logger.info(f"JOB_ANALYSIS_SUCCESS - Retrieved {len(jobs)} jobs after AI analysis")
            return jobs
            
        except Exception as e:
            self.logger.error(f"Enhanced job listing retrieval failed: {e}")
            self.detailed_logger.error(f"JOB_ANALYSIS_ERROR - Enhanced job analysis failed: {e}")
            return []
    
    def _extract_job_data_enhanced(self, job_element, job_number: int) -> Optional[Dict[str, Any]]:
        """Extract comprehensive job data with enhanced selectors"""
        try:
            # Extract basic information
            title = self._extract_job_title_enhanced(job_element)
            company = self._extract_company_name_enhanced(job_element)
            location = self._extract_job_location(job_element)
            salary = self._extract_job_salary(job_element)
            job_url = self._extract_job_url(job_element)
            
            if not title or not company:
                self.logger.warning(f"Could not extract title/company from job {job_number}")
                return None
            
            # Extract additional details
            description = self._extract_job_description(job_element)
            easy_apply = self._check_easy_apply_enhanced(job_element)
            
            job_data = {
                'title': title,
                'company': company,
                'location': location,
                'salary': salary,
                'job_url': job_url,
                'description': description,
                'easy_apply': easy_apply,
                'extracted_at': datetime.now().isoformat()
            }
            
            self.logger.info(f"Successfully extracted data for job {job_number}: {title} at {company}")
            return job_data
            
        except Exception as e:
            self.logger.warning(f"Error extracting job data for job {job_number}: {e}")
            return None
    
    def _extract_job_title_enhanced(self, job_element) -> str:
        """Enhanced job title extraction"""
        title_selectors = [
            ".//a[contains(@class, 'job-card-list__title')]",
            ".//a[contains(@class, 'job-card-container__link')]",
            ".//h3[contains(@class, 'job-card-list__title')]",
            ".//span[contains(@class, 'job-card-list__title')]",
            ".//a[contains(@data-control-name, 'job_card_click')]",
            ".//a[contains(@class, 'base-card__full-link')]",
            ".//h3[contains(@class, 'base-search-card__title')]",
            ".//a[contains(@class, 'base-search-card__title')]",
            ".//span[contains(@class, 'base-search-card__title')]",
            ".//a[contains(@data-entity-urn, 'job')]",
            ".//h3",
            ".//a[contains(@href, '/jobs/view/')]"
        ]
        
        for selector in title_selectors:
            try:
                element = job_element.find_element(By.XPATH, selector)
                title = element.text.strip()
                if title:
                    return title
            except NoSuchElementException:
                continue
        
        return ""
    
    def _extract_company_name_enhanced(self, job_element) -> str:
        """Enhanced company name extraction"""
        company_selectors = [
            ".//h4[contains(@class, 'job-card-container__company-name')]",
            ".//a[contains(@class, 'job-card-container__company-name')]",
            ".//h4[contains(@class, 'base-search-card__subtitle')]",
            ".//a[contains(@class, 'base-search-card__subtitle')]",
            ".//span[contains(@class, 'job-card-container__company-name')]",
            ".//div[contains(@class, 'job-card-container__company-name')]",
            ".//h4",
            ".//a[contains(@href, '/company/')]"
        ]
        
        for selector in company_selectors:
            try:
                element = job_element.find_element(By.XPATH, selector)
                company = element.text.strip()
                if company:
                    return company
            except NoSuchElementException:
                continue
        
        return ""
    
    def _extract_job_location(self, job_element) -> str:
        """Extract job location"""
        location_selectors = [
            ".//span[contains(@class, 'job-card-container__metadata-item')]",
            ".//li[contains(@class, 'job-card-container__metadata-item')]",
            ".//span[contains(@class, 'job-card-container__metadata-wrapper')]//span",
            ".//div[contains(@class, 'job-card-container__metadata')]//span"
        ]
        
        for selector in location_selectors:
            try:
                elements = job_element.find_elements(By.XPATH, selector)
                for element in elements:
                    text = element.text.strip()
                    if text and any(keyword in text.lower() for keyword in ['remote', 'hybrid', 'on-site', 'location']):
                        return text
            except NoSuchElementException:
                continue
        
        return ""
    
    def _extract_job_salary(self, job_element) -> str:
        """Extract job salary information"""
        salary_selectors = [
            ".//span[contains(@class, 'job-card-container__metadata-item')]",
            ".//li[contains(@class, 'job-card-container__metadata-item')]"
        ]
        
        for selector in salary_selectors:
            try:
                elements = job_element.find_elements(By.XPATH, selector)
                for element in elements:
                    text = element.text.strip()
                    if '$' in text or 'salary' in text.lower() or 'compensation' in text.lower():
                        return text
            except NoSuchElementException:
                continue
        
        return ""
    
    def _extract_job_url(self, job_element) -> str:
        """Extract job URL"""
        url_selectors = [
            ".//a[contains(@class, 'job-card-list__title')]",
            ".//a[contains(@class, 'job-card-container__link')]",
            ".//a[contains(@data-control-name, 'job_card_click')]",
            ".//a[contains(@href, '/jobs/view/')]"
        ]
        
        for selector in url_selectors:
            try:
                element = job_element.find_element(By.XPATH, selector)
                url = element.get_attribute('href')
                if url:
                    return url
            except NoSuchElementException:
                continue
        
        return ""
    
    def _extract_job_description(self, job_element) -> str:
        """Extract job description (if available)"""
        try:
            # Try to click on job to get description
            clickable_element = job_element.find_element(By.XPATH, ".//a")
            clickable_element.click()
            time.sleep(2)
            
            # Look for description
            description_selectors = [
                "//div[contains(@class, 'jobs-description-content__text')]",
                "//div[contains(@class, 'jobs-box__html-content')]",
                "//div[contains(@class, 'jobs-description')]"
            ]
            
            for selector in description_selectors:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    description = element.text.strip()
                    if description:
                        return description[:1000]  # Limit length
                except NoSuchElementException:
                    continue
            
            return ""
            
        except Exception as e:
            self.logger.debug(f"Could not extract job description: {e}")
            return ""
    
    def _check_easy_apply_enhanced(self, job_element) -> bool:
        """Enhanced Easy Apply detection"""
        easy_apply_selectors = [
            ".//button[contains(@aria-label, 'Easy Apply')]",
            ".//button[contains(@class, 'jobs-apply-button')]",
            ".//span[contains(text(), 'Easy Apply')]",
            ".//button[contains(text(), 'Easy Apply')]"
        ]
        
        for selector in easy_apply_selectors:
            try:
                element = job_element.find_element(By.XPATH, selector)
                if element:
                    return True
            except NoSuchElementException:
                continue
        
        return False
    
    def apply_to_job_enhanced(self, job_data: Dict[str, Any]) -> bool:
        """Enhanced job application with AI optimization"""
        try:
            self.logger.info(f"Starting enhanced application for: {job_data['title']} at {job_data['company']}")
            self.detailed_logger.info(f"APPLICATION_START - Enhanced application for: {job_data['title']} at {job_data['company']}")
            
            # Check daily limits
            can_apply, reason = self.scheduler.can_apply_now()
            if not can_apply:
                self.logger.warning(f"Cannot apply: {reason}")
                self.detailed_logger.warning(f"APPLICATION_BLOCKED - {reason}")
                return False
            
            # Navigate to job if needed
            if job_data.get('job_url'):
                self.driver.get(job_data['job_url'])
                time.sleep(random.uniform(2, 4))
            
            # Find and click Easy Apply button
            easy_apply_button = self._find_easy_apply_button_enhanced()
            if not easy_apply_button:
                self.logger.warning("Easy Apply button not found")
                self.detailed_logger.warning("APPLICATION_FAILED - Easy Apply button not found")
                return False
            
            easy_apply_button.click()
            time.sleep(random.uniform(2, 4))
            
            # Handle application form with AI optimization
            success = self._handle_application_form_enhanced(job_data)
            
            if success:
                # Record application in database
                application = JobApplication(
                    job_title=job_data['title'],
                    company=job_data['company'],
                    job_url=job_data.get('job_url', ''),
                    application_date=datetime.now(),
                    status='applied',
                    easy_apply=job_data.get('easy_apply', False),
                    notes=f"AI Match Score: {job_data.get('ai_match', {}).get('score', 'N/A')}",
                    salary_range=job_data.get('salary', ''),
                    location=job_data.get('location', ''),
                    job_description=job_data.get('description', '')
                )
                
                app_id = self.db_manager.add_job_application(application)
                self.scheduler.record_application()
                self.applications_sent += 1
                
                self.logger.info(f"Successfully applied to job (ID: {app_id})")
                self.detailed_logger.info(f"APPLICATION_SUCCESS - Applied to {job_data['title']} at {job_data['company']} (ID: {app_id})")
                
                # Cooldown between applications
                cooldown = random.uniform(
                    self.scheduler.config.get('cooldown_between_applications', 60),
                    self.scheduler.config.get('cooldown_between_applications', 60) + 30
                )
                time.sleep(cooldown)
                
                return True
            else:
                self.logger.warning("Application form handling failed")
                self.detailed_logger.warning("APPLICATION_FAILED - Form handling failed")
                return False
                
        except Exception as e:
            self.logger.error(f"Enhanced application failed: {e}")
            self.detailed_logger.error(f"APPLICATION_ERROR - Enhanced application failed: {e}")
            return False
    
    def _find_easy_apply_button_enhanced(self):
        """Enhanced Easy Apply button detection"""
        easy_apply_selectors = [
            "//button[contains(@aria-label, 'Easy Apply')]",
            "//button[contains(@class, 'jobs-apply-button')]",
            "//span[contains(text(), 'Easy Apply')]/parent::button",
            "//button[contains(text(), 'Easy Apply')]",
            "//button[contains(@class, 'jobs-apply-button--top-card')]"
        ]
        
        for selector in easy_apply_selectors:
            try:
                element = self.wait.until(EC.element_to_be_clickable((By.XPATH, selector)))
                return element
            except TimeoutException:
                continue
        
        return None
    
    def _handle_application_form_enhanced(self, job_data: Dict[str, Any]) -> bool:
        """Enhanced application form handling with AI optimization"""
        try:
            # Handle multiple pages of application form
            max_pages = 5
            for page in range(max_pages):
                self.logger.info(f"Handling application form page {page + 1}")
                
                # Fill form fields with AI-optimized responses
                if not self._fill_form_fields_enhanced(job_data):
                    self.logger.warning(f"Failed to fill form fields on page {page + 1}")
                    return False
                
                # Look for next button
                next_button = self._find_next_button()
                if next_button:
                    next_button.click()
                    time.sleep(random.uniform(2, 4))
                else:
                    # Look for submit button
                    submit_button = self._find_submit_button()
                    if submit_button:
                        submit_button.click()
                        time.sleep(random.uniform(3, 5))
                        return True
                    else:
                        self.logger.warning("No next or submit button found")
                        return False
            
            self.logger.warning("Maximum form pages reached")
            return False
            
        except Exception as e:
            self.logger.error(f"Enhanced form handling failed: {e}")
            return False
    
    def _fill_form_fields_enhanced(self, job_data: Dict[str, Any]) -> bool:
        """Fill form fields with AI-optimized responses"""
        try:
            # Get AI-optimized resume keywords
            if self.resume_optimization and job_data.get('description'):
                keywords = self.ai_matcher.optimize_resume_keywords(
                    self.user_profile, 
                    job_data['description']
                )
                self.logger.info(f"AI suggested keywords: {keywords}")
            
            # Fill common form fields
            form_fields = [
                ("phone", self.config.phone or ""),
                ("email", self.config.email),
                ("resume", "optimized_resume.pdf"),  # Would use AI-optimized resume
                ("cover_letter", self._generate_cover_letter(job_data))
            ]
            
            for field_type, value in form_fields:
                if value:
                    self._fill_field_by_type(field_type, value)
            
            return True
            
        except Exception as e:
            self.logger.error(f"Enhanced form filling failed: {e}")
            return False
    
    def _generate_cover_letter(self, job_data: Dict[str, Any]) -> str:
        """Generate AI-optimized cover letter"""
        # This would integrate with an AI service like OpenAI
        # For now, return a template
        return f"""
Dear Hiring Manager,

I am excited to apply for the {job_data['title']} position at {job_data['company']}. 
With my background in {', '.join(self.user_profile.skills[:3])} and {self.user_profile.experience_years} years of experience, 
I am confident I would be a valuable addition to your team.

Best regards,
[Your Name]
        """.strip()
    
    def _fill_field_by_type(self, field_type: str, value: str):
        """Fill form field by type"""
        field_selectors = {
            "phone": ["//input[@type='tel']", "//input[contains(@name, 'phone')]"],
            "email": ["//input[@type='email']", "//input[contains(@name, 'email')]"],
            "resume": ["//input[@type='file']", "//input[contains(@name, 'resume')]"],
            "cover_letter": ["//textarea", "//input[contains(@name, 'cover')]"]
        }
        
        selectors = field_selectors.get(field_type, [])
        for selector in selectors:
            try:
                element = self.driver.find_element(By.XPATH, selector)
                if field_type == "resume":
                    # Handle file upload
                    element.send_keys(value)
                else:
                    element.clear()
                    element.send_keys(value)
                time.sleep(random.uniform(0.5, 1.5))
                return
            except NoSuchElementException:
                continue
    
    def _find_next_button(self):
        """Find next button in application form"""
        next_selectors = [
            "//button[contains(text(), 'Next')]",
            "//button[contains(text(), 'Continue')]",
            "//button[contains(@aria-label, 'Continue')]",
            "//button[contains(@class, 'jobs-apply-button')]"
        ]
        
        for selector in next_selectors:
            try:
                element = self.driver.find_element(By.XPATH, selector)
                if element.is_enabled():
                    return element
            except NoSuchElementException:
                continue
        
        return None
    
    def _find_submit_button(self):
        """Find submit button in application form"""
        submit_selectors = [
            "//button[contains(text(), 'Submit')]",
            "//button[contains(text(), 'Send application')]",
            "//button[contains(@aria-label, 'Submit')]",
            "//button[contains(@class, 'jobs-apply-button')]"
        ]
        
        for selector in submit_selectors:
            try:
                element = self.driver.find_element(By.XPATH, selector)
                if element.is_enabled():
                    return element
            except NoSuchElementException:
                continue
        
        return None
    
    def run_automation_enhanced(self) -> Dict[str, Any]:
        """Run enhanced automation with full features"""
        try:
            self.logger.info("Starting enhanced LinkedIn automation")
            self.detailed_logger.info("AUTOMATION_START - Enhanced automation session started")
            
            # Start session
            if not self.start_session():
                return {"success": False, "error": "Failed to start session"}
            
            # Login
            if not self.login():
                return {"success": False, "error": "Failed to login"}
            
            # Search jobs
            if not self.search_jobs_enhanced():
                return {"success": False, "error": "Failed to search jobs"}
            
            # Get and process jobs
            jobs = self.get_job_listings_enhanced()
            if not jobs:
                return {"success": False, "error": "No jobs found"}
            
            # Apply to jobs
            successful_applications = 0
            for job in jobs:
                if self.apply_to_job_enhanced(job):
                    successful_applications += 1
                
                # Check if we've reached daily limit
                if not self.scheduler.can_apply_now()[0]:
                    self.logger.info("Daily application limit reached")
                    break
            
            # Record search session
            if self.current_search_session:
                self.current_search_session.jobs_found = len(jobs)
                self.current_search_session.applications_sent = successful_applications
                self.current_search_session.success_rate = (successful_applications / len(jobs) * 100) if jobs else 0
                self.current_search_session.session_duration = int((datetime.now() - self.session_start_time).total_seconds() / 60)
                
                self.db_manager.add_job_search_session(self.current_search_session)
            
            result = {
                "success": True,
                "jobs_found": len(jobs),
                "applications_sent": successful_applications,
                "success_rate": (successful_applications / len(jobs) * 100) if jobs else 0,
                "session_duration": int((datetime.now() - self.session_start_time).total_seconds() / 60)
            }
            
            self.logger.info(f"Enhanced automation completed: {result}")
            self.detailed_logger.info(f"AUTOMATION_SUCCESS - Enhanced automation completed: {result}")
            
            return result
            
        except Exception as e:
            self.logger.error(f"Enhanced automation failed: {e}")
            self.detailed_logger.error(f"AUTOMATION_ERROR - Enhanced automation failed: {e}")
            return {"success": False, "error": str(e)}
        
        finally:
            self.close_session()
    
    def close_session(self):
        """Close browser session"""
        try:
            if self.driver:
                self.driver.quit()
                self.logger.info("Enhanced browser session closed")
                self.detailed_logger.info("SESSION_END - Enhanced browser session closed")
        except Exception as e:
            self.logger.error(f"Error closing enhanced session: {e}")
    
    def get_application_stats(self) -> Dict[str, Any]:
        """Get comprehensive application statistics"""
        try:
            # Get database stats
            analytics = self.db_manager.get_analytics(30)
            daily_stats = self.scheduler.get_daily_progress()
            
            return {
                "database_stats": analytics,
                "daily_progress": daily_stats,
                "session_stats": {
                    "applications_sent": self.applications_sent,
                    "jobs_processed": self.jobs_processed,
                    "session_duration": int((datetime.now() - self.session_start_time).total_seconds() / 60) if self.session_start_time else 0
                }
            }
        except Exception as e:
            self.logger.error(f"Error getting application stats: {e}")
            return {}
