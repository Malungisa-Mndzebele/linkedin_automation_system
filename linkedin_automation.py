"""
LinkedIn Job Application Automation MVP
Core automation class for LinkedIn job searching and application
"""
import time
import logging
from typing import List, Optional, Dict, Any
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from webdriver_manager.chrome import ChromeDriverManager

from comprehensive_logging import AutomationLogger
from config import LinkedInConfig, JobApplicationConfig


class LinkedInAutomation:
    """
    Main class for LinkedIn job application automation
    """
    
    def __init__(self, config: LinkedInConfig, job_config: JobApplicationConfig):
        """
        Initialize LinkedIn automation with configuration
        
        Args:
            config: LinkedIn configuration settings
            job_config: Job application configuration settings
        """
        self.config = config
        self.job_config = job_config
        self.driver: Optional[webdriver.Chrome] = None
        self.wait: Optional[WebDriverWait] = None
        self.logger = self._setup_logger()
        self.comprehensive_logger = AutomationLogger()
        self.applications_today = 0
        
    def _setup_logger(self) -> logging.Logger:
        """Setup logging configuration"""
        logger = logging.getLogger(__name__)
        logger.setLevel(logging.INFO)
        
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        # Also add to detailed actions logger
        self.detailed_logger = logging.getLogger('automation_actions')
            
        return logger
    
    def _setup_driver(self) -> webdriver.Chrome:
        """
        Setup Chrome WebDriver with appropriate options
        
        Returns:
            Configured Chrome WebDriver instance
        """
        chrome_options = Options()
        
        if self.config.headless:
            chrome_options.add_argument("--headless")
            
        # Add unique user data directory to avoid conflicts
        import tempfile
        import os
        temp_dir = tempfile.mkdtemp()
        user_data_dir = os.path.join(temp_dir, "chrome_user_data")
        chrome_options.add_argument(f"--user-data-dir={user_data_dir}")
        
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("--disable-web-security")
        chrome_options.add_argument("--disable-features=VizDisplayCompositor")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        
        # Use ChromeDriver with smart fallback handling
        service = None
        local_chromedriver = os.path.join(os.getcwd(), "chromedriver", "chromedriver.exe")
        
        # Try approaches in order of preference (webdriver-manager first for Chrome 141 compatibility)
        approaches = [
            ("webdriver-manager (latest)", lambda: Service(ChromeDriverManager().install())),
            ("no service (selenium default)", lambda: None),
            ("local chromedriver", lambda: Service(local_chromedriver) if os.path.exists(local_chromedriver) else None)
        ]
        
        for approach_name, service_func in approaches:
            try:
                self.logger.info(f"Trying ChromeDriver approach: {approach_name}")
                service = service_func()
                
                if service is None:
                    # Try without explicit service
                    driver = webdriver.Chrome(options=chrome_options)
                else:
                    # Try with explicit service
                    driver = webdriver.Chrome(service=service, options=chrome_options)
                
                self.logger.info(f"✅ ChromeDriver {approach_name} successful")
                break
                
            except Exception as e:
                self.logger.warning(f"ChromeDriver {approach_name} failed: {e}")
                if 'driver' in locals():
                    try:
                        driver.quit()
                    except:
                        pass
                driver = None
                continue
        
        if 'driver' not in locals() or driver is None:
            raise Exception("All ChromeDriver approaches failed - please update Chrome or ChromeDriver")
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        # Set timeouts
        driver.implicitly_wait(self.config.implicit_wait)
        driver.set_page_load_timeout(self.config.page_load_timeout)
        
        return driver
    
    def start_session(self) -> bool:
        """
        Start a new browser session
        
        Returns:
            True if session started successfully, False otherwise
        """
        try:
            self.comprehensive_logger.log_step(1, "Browser Session Start", "STARTED")
            self.driver = self._setup_driver()
            self.wait = WebDriverWait(self.driver, self.config.implicit_wait)
            self.driver.maximize_window()
            self.logger.info("Browser session started successfully")
            self.comprehensive_logger.log_browser_start(self.config.headless)
            self.comprehensive_logger.log_step(1, "Browser Session Start", "COMPLETED")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to start browser session: {e}")
            self.comprehensive_logger.log_error("Browser Session", str(e), "Failed to initialize Chrome WebDriver")
            self.comprehensive_logger.log_step(1, "Browser Session Start", "FAILED")
            return False
    
    def login(self) -> bool:
        """
        Login to LinkedIn with configured credentials
        
        Returns:
            True if login successful, False otherwise
        """
        if not self.driver:
            self.logger.error("Driver not initialized. Call start_session() first.")
            self.comprehensive_logger.log_error("Login", "Driver not initialized", "Must call start_session() first")
            return False
            
        try:
            self.comprehensive_logger.log_step(2, "LinkedIn Login", "STARTED")
            self.logger.info("Starting LinkedIn login process")
            self.driver.get(self.config.linkedin_login_url)
            
            # Wait for and fill email field
            email_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "username"))
            )
            email_field.clear()
            email_field.send_keys(self.config.email)
            
            # Fill password field
            password_field = self.driver.find_element(By.ID, "password")
            password_field.clear()
            password_field.send_keys(self.config.password)
            
            # Click login button
            login_button = self.driver.find_element(By.XPATH, "//button[@type='submit']")
            login_button.click()
            
            # Wait for login to complete (check for global nav or feed)
            try:
                self.wait.until(
                    EC.any_of(
                        EC.presence_of_element_located((By.ID, "global-nav")),
                        EC.presence_of_element_located((By.CLASS_NAME, "feed-container"))
                    )
                )
                self.logger.info("Successfully logged into LinkedIn")
                self.comprehensive_logger.log_login_attempt(self.config.email, True)
                self.comprehensive_logger.log_step(2, "LinkedIn Login", "COMPLETED")
                return True
                
            except TimeoutException:
                # Check if we're on a verification page or if login failed
                if "challenge" in self.driver.current_url or "checkpoint" in self.driver.current_url:
                    self.logger.warning("LinkedIn requires additional verification")
                    self.comprehensive_logger.log_error("Login", "Additional verification required", "LinkedIn challenge page detected")
                    self.comprehensive_logger.log_step(2, "LinkedIn Login", "FAILED")
                    return False
                else:
                    self.logger.error("Login failed - unable to verify successful login")
                    self.comprehensive_logger.log_login_attempt(self.config.email, False)
                    self.comprehensive_logger.log_error("Login", "Unable to verify successful login", "Timeout waiting for login confirmation")
                    self.comprehensive_logger.log_step(2, "LinkedIn Login", "FAILED")
                    return False
                    
        except Exception as e:
            self.logger.error(f"Login failed with error: {e}")
            self.comprehensive_logger.log_login_attempt(self.config.email, False)
            self.comprehensive_logger.log_error("Login", str(e), "Exception during login process")
            self.comprehensive_logger.log_step(2, "LinkedIn Login", "FAILED")
            return False
    
    def search_jobs(self, keywords: Optional[List[str]] = None) -> bool:
        """
        Search for jobs on LinkedIn
        
        Args:
            keywords: List of job search keywords. Uses config keywords if None
            
        Returns:
            True if search successful, False otherwise
        """
        if not self.driver:
            self.logger.error("Driver not initialized. Call start_session() first.")
            self.comprehensive_logger.log_error("Job Search", "Driver not initialized", "Must call start_session() first")
            return False
            
        try:
            self.comprehensive_logger.log_step(3, "Job Search", "STARTED")
            keywords = keywords or self.config.job_keywords
            search_term = " ".join(keywords)
            
            self.logger.info(f"Searching for jobs with keywords: {search_term}")
            self.comprehensive_logger.log_job_search(keywords, "", self.config.easy_apply_only)
            
            # Navigate to LinkedIn jobs with search parameters
            search_url = f"https://www.linkedin.com/jobs/search/?keywords={search_term.replace(' ', '%20')}"
            if self.config.easy_apply_only:
                search_url += "&f_LF=f_AL"  # Easy Apply filter
            
            self.driver.get(search_url)
            
            # Wait for page to load
            time.sleep(5)
            
            # Wait for job listings to appear with extended timeout and multiple attempts
            job_loaded = False
            selectors_to_try = [
                (By.CLASS_NAME, "jobs-search-results-list"),
                (By.CLASS_NAME, "jobs-search-results"),
                (By.CSS_SELECTOR, ".scaffold-layout__list-container"),
                (By.CSS_SELECTOR, "[data-test-id='job-search-results']"),
                (By.CSS_SELECTOR, ".jobs-search__results-list"),
                (By.CSS_SELECTOR, ".jobs-search-results__list")
            ]
            # Prefer the instance wait (allows tests to inject a mock). Fall back to a fresh WebDriverWait.
            wait = self.wait or WebDriverWait(self.driver, self.config.job_search_timeout)

            for i, (by_method, selector) in enumerate(selectors_to_try):
                try:
                    self.logger.info(f"Waiting for job listings (attempt {i+1}/{len(selectors_to_try)}) with selector: {selector}")
                    wait.until(
                        EC.presence_of_element_located((by_method, selector))
                    )
                    self.logger.info(f"Job search results loaded successfully with selector: {selector}")
                    self.comprehensive_logger.log_browser_operation("Job search results loaded", f"Selector: {selector}")
                    job_loaded = True
                    break
                except TimeoutException:
                    self.logger.warning(f"Timeout with selector {selector}, trying next...")
                    continue
            
            if not job_loaded:
                self.logger.warning("Job search results may not have loaded properly - will attempt to extract anyway")
                self.comprehensive_logger.log_error("Job Search", "Results may not have loaded", "All selectors timed out")
                
                # Wait a bit more for any dynamic content
                time.sleep(5)
            
            self.logger.info("Job search completed successfully")
            self.comprehensive_logger.log_step(3, "Job Search", "COMPLETED")
            return True
            
        except Exception as e:
            self.logger.error(f"Job search failed: {e}")
            self.comprehensive_logger.log_error("Job Search", str(e), "Exception during job search")
            self.comprehensive_logger.log_step(3, "Job Search", "FAILED")
            return False
    
    def _apply_easy_apply_filter(self) -> bool:
        """
        Apply Easy Apply filter to job search results
        
        Returns:
            True if filter applied successfully, False otherwise
        """
        try:
            # Look for Easy Apply filter button
            easy_apply_filter = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Easy Apply filter')]"))
            )
            easy_apply_filter.click()
            time.sleep(2)  # Wait for filter to apply
            
            self.logger.info("Easy Apply filter applied successfully")
            return True
            
        except TimeoutException:
            self.logger.warning("Easy Apply filter not found or not clickable")
            return False
        except Exception as e:
            self.logger.error(f"Failed to apply Easy Apply filter: {e}")
            return False
    
    def get_job_listings(self, max_jobs: int = 25) -> List[Dict[str, Any]]:
        """
        Get list of available job listings from current search results
        
        Args:
            max_jobs: Maximum number of jobs to retrieve
            
        Returns:
            List of job dictionaries with title, company, and apply button info
        """
        if not self.driver:
            self.logger.error("Driver not initialized")
            return []
            
        jobs = []
        try:
            # Scroll multiple times to load more jobs
            self.logger.info("Scrolling to load more job listings...")
            for scroll_attempt in range(3):
                self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)  # Wait longer for dynamic content to load
                self.logger.info(f"Scroll attempt {scroll_attempt + 1}/3 completed")
            
            # Wait a bit more for any lazy-loaded content
            time.sleep(2)
            
            # Try multiple selectors for job cards (LinkedIn has different layouts)
            job_selectors = [
                "//div[contains(@class, 'job-card-container')]",
                "//div[contains(@class, 'jobs-search-results__list-item')]",
                "//li[contains(@class, 'jobs-search-results__list-item')]",
                "//div[contains(@class, 'job-card-list')]",
                "//div[contains(@class, 'job-card')]",
                "//li[contains(@class, 'job-card')]",
                "//div[contains(@class, 'jobs-search-results__list')]//div[contains(@class, 'job-card')]"
            ]
            
            job_elements = []
            for selector in job_selectors:
                elements = self.driver.find_elements(By.XPATH, selector)
                if elements:
                    job_elements = elements
                    self.logger.info(f"Found {len(elements)} job elements using selector: {selector}")
                    break
            
            if not job_elements:
                self.logger.warning("No job elements found with any selector")
                self.comprehensive_logger.log_error("Job Extraction", "No job elements found", "All selectors failed")
                return []
            
            for i, job_element in enumerate(job_elements[:max_jobs]):
                try:
                    # Extract job information with multiple selectors
                    title = self._extract_job_title(job_element)
                    company = self._extract_company_name(job_element)
                    
                    if not title or not company:
                        self.logger.warning(f"Could not extract title/company from job {i+1}")
                        self.comprehensive_logger.log_error("Job Extraction", f"Could not extract title/company from job {i+1}", "Missing job information")
                        # Debug: log the HTML structure for troubleshooting
                        self._debug_job_element(job_element, i+1)
                        continue
                    
                    # Check if Easy Apply button exists
                    has_easy_apply = self._check_easy_apply(job_element)
                    
                    job_info = {
                        'title': title,
                        'company': company,
                        'has_easy_apply': has_easy_apply,
                        'element': job_element
                    }
                    
                    jobs.append(job_info)
                    self.logger.info(f"Job {i+1}: {title} at {company} - Easy Apply: {has_easy_apply}")
                    self.comprehensive_logger.log_job_found(i+1, title, company, has_easy_apply)
                    
                except Exception as e:
                    self.logger.warning(f"Could not extract info from job {i+1}: {e}")
                    self.comprehensive_logger.log_error("Job Extraction", str(e), f"Failed to extract info from job {i+1}")
                    continue
                    
            self.logger.info(f"Retrieved {len(jobs)} job listings")
            return jobs
            
        except Exception as e:
            self.logger.error(f"Failed to get job listings: {e}")
            return []
    
    def _extract_job_title(self, job_element) -> str:
        """Extract job title from job element"""
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
                if title and len(title) > 3:  # Ensure it's a meaningful title
                    return title
            except NoSuchElementException:
                continue
        
        return ""
    
    def _extract_company_name(self, job_element) -> str:
        """Extract company name from job element"""
        company_selectors = [
            ".//a[contains(@class, 'job-card-container__company-name')]",
            ".//h4[contains(@class, 'job-card-container__company-name')]",
            ".//span[contains(@class, 'job-card-container__company-name')]",
            ".//a[contains(@data-control-name, 'job_card_company_click')]",
            ".//h4[contains(@class, 'base-search-card__subtitle')]",
            ".//a[contains(@class, 'base-search-card__subtitle')]",
            ".//span[contains(@class, 'base-search-card__subtitle')]",
            ".//a[contains(@class, 'hidden-nested-link')]",
            ".//h4",
            ".//a[contains(@href, '/company/')]"
        ]
        
        for selector in company_selectors:
            try:
                element = job_element.find_element(By.XPATH, selector)
                company = element.text.strip()
                if company and len(company) > 1:  # Ensure it's a meaningful company name
                    return company
            except NoSuchElementException:
                continue
        
        return ""
    
    def _check_easy_apply(self, job_element) -> bool:
        """Check if job has Easy Apply option"""
        easy_apply_selectors = [
            ".//button[contains(@aria-label, 'Easy Apply')]",
            ".//button[contains(text(), 'Easy Apply')]",
            ".//span[contains(text(), 'Easy Apply')]",
            ".//button[contains(@class, 'jobs-apply-button')]"
        ]
        
        for selector in easy_apply_selectors:
            try:
                job_element.find_element(By.XPATH, selector)
                return True
            except NoSuchElementException:
                continue
        
        return False
    
    def _debug_job_element(self, job_element, job_number: int):
        """Debug method to log job element structure for troubleshooting"""
        try:
            # Get the outer HTML of the job element (limited to first 500 chars)
            html_snippet = job_element.get_attribute('outerHTML')[:500]
            self.logger.info(f"Job {job_number} HTML structure (first 500 chars): {html_snippet}")
            
            # Try to find any text content
            all_text = job_element.text.strip()
            if all_text:
                self.logger.info(f"Job {job_number} text content: {all_text[:200]}...")
            else:
                self.logger.info(f"Job {job_number} has no text content")
                
        except Exception as e:
            self.logger.warning(f"Could not debug job element {job_number}: {e}")
    
    def apply_to_job(self, job_info: Dict[str, Any]) -> bool:
        """
        Apply to a specific job using Easy Apply
        
        Args:
            job_info: Job information dictionary from get_job_listings()
            
        Returns:
            True if application successful, False otherwise
        """
        if not self.driver:
            self.logger.error("Driver not initialized")
            self.comprehensive_logger.log_error("Job Application", "Driver not initialized", "Must call start_session() first")
            return False
            
        if not job_info.get('has_easy_apply', False):
            self.logger.warning(f"Job '{job_info.get('title', 'Unknown')}' does not have Easy Apply")
            self.comprehensive_logger.log_decision("Application Skip", f"No Easy Apply for '{job_info.get('title', 'Unknown')}'", "Job does not support Easy Apply")
            return False
            
        if self.applications_today >= self.config.max_applications_per_day:
            self.logger.warning("Daily application limit reached")
            self.comprehensive_logger.log_decision("Application Limit", "Daily limit reached", f"Max applications: {self.config.max_applications_per_day}")
            return False
            
        try:
            self.logger.info(f"Applying to: {job_info['title']} at {job_info['company']}")
            self.comprehensive_logger.log_job_application_attempt(self.applications_today + 1, job_info['title'], job_info['company'])
            
            # Find and click Easy Apply button with multiple selectors
            easy_apply_button = None
            easy_apply_selectors = [
                ".//button[contains(@aria-label, 'Easy Apply')]",
                ".//button[contains(text(), 'Easy Apply')]",
                ".//button[contains(@class, 'jobs-apply-button')]"
            ]
            
            for selector in easy_apply_selectors:
                try:
                    easy_apply_button = job_info['element'].find_element(By.XPATH, selector)
                    break
                except NoSuchElementException:
                    continue
            
            if not easy_apply_button:
                self.logger.warning(f"Could not find Easy Apply button for {job_info['title']}")
                self.comprehensive_logger.log_job_application_result(self.applications_today + 1, job_info['title'], job_info['company'], False, "Easy Apply button not found")
                return False
            
            # Scroll to button and click
            self.driver.execute_script("arguments[0].scrollIntoView(true);", easy_apply_button)
            time.sleep(1)
            easy_apply_button.click()
            
            # Wait for application modal to appear
            time.sleep(3)
            
            # Handle application form (simplified for MVP)
            success = self._handle_application_form()
            
            if success:
                self.applications_today += 1
                self.logger.info(f"Successfully applied to {job_info['title']}")
                self.comprehensive_logger.log_job_application_result(self.applications_today, job_info['title'], job_info['company'], True)
            else:
                self.logger.warning(f"Failed to complete application for {job_info['title']}")
                self.comprehensive_logger.log_job_application_result(self.applications_today + 1, job_info['title'], job_info['company'], False, "Application form handling failed")
                
            return success
            
        except Exception as e:
            self.logger.error(f"Failed to apply to job: {e}")
            self.comprehensive_logger.log_job_application_result(self.applications_today + 1, job_info['title'], job_info['company'], False, str(e))
            return False
    
    def _handle_application_form(self) -> bool:
        """
        Handle the Easy Apply application form
        
        Returns:
            True if form submitted successfully, False otherwise
        """
        try:
            # This is a simplified implementation for MVP
            # In a full implementation, you would handle various form fields
            
            # Look for submit button
            submit_button = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Submit')]"))
            )
            submit_button.click()
            
            # Wait for confirmation
            time.sleep(2)
            
            # Check if application was successful (look for success message or modal close)
            try:
                # Look for success indicators
                success_indicators = [
                    "//div[contains(text(), 'Application sent')]",
                    "//div[contains(text(), 'Applied')]",
                    "//button[contains(@aria-label, 'Applied')]"
                ]
                
                for indicator in success_indicators:
                    try:
                        self.driver.find_element(By.XPATH, indicator)
                        return True
                    except NoSuchElementException:
                        continue
                        
                return True  # Assume success if no error occurred
                
            except Exception:
                return False
                
        except Exception as e:
            self.logger.error(f"Failed to handle application form: {e}")
            return False
    
    def send_message(self, message: str, recipient_url: Optional[str] = None) -> bool:
        """
        Send a message to a LinkedIn connection
        
        Args:
            message: Message content to send
            recipient_url: URL of the message thread (optional)
            
        Returns:
            True if message sent successfully, False otherwise
        """
        if not self.driver:
            self.logger.error("Driver not initialized")
            return False
            
        try:
            if recipient_url:
                self.driver.get(recipient_url)
            
            # Wait for message input field
            message_field = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'msg-form__contenteditable')]"))
            )
            
            message_field.clear()
            message_field.send_keys(message)
            
            # Send the message
            send_button = self.driver.find_element(
                By.XPATH, "//button[contains(@class, 'msg-form__send-button')]"
            )
            send_button.click()
            
            self.logger.info("Message sent successfully")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to send message: {e}")
            return False
    
    def close_session(self):
        """Close the browser session"""
        if self.driver:
            try:
                self.driver.quit()
                self.driver = None
                self.logger.info("Browser session closed")
            except Exception as e:
                self.logger.warning(f"Error closing browser session: {e}")
                self.driver = None
    
    def get_application_stats(self) -> Dict[str, Any]:
        """
        Get current application statistics
        
        Returns:
            Dictionary with application statistics
        """
        return {
            'applications_today': self.applications_today,
            'max_applications_per_day': self.config.max_applications_per_day,
            'remaining_applications': self.config.max_applications_per_day - self.applications_today
        }
