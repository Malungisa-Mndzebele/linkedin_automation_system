"""
Configuration management for LinkedIn Job Application Automation MVP
"""
import os
from typing import Optional
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class LinkedInConfig(BaseModel):
    """Configuration model for LinkedIn automation"""
    
    # Credentials
    email: str = Field(..., description="LinkedIn email address")
    password: str = Field(..., description="LinkedIn password")
    
    # Job search settings
    job_keywords: list[str] = Field(default=["Data Analyst"], description="Job search keywords")
    easy_apply_only: bool = Field(default=True, description="Only apply to Easy Apply jobs")
    max_applications_per_day: int = Field(default=10, description="Maximum applications per day")
    
    # Browser settings
    headless: bool = Field(default=False, description="Run browser in headless mode")
    implicit_wait: int = Field(default=10, description="Implicit wait time in seconds")
    page_load_timeout: int = Field(default=30, description="Page load timeout in seconds")
    
    # URLs
    linkedin_login_url: str = Field(default="https://www.linkedin.com/login", description="LinkedIn login URL")
    linkedin_jobs_url: str = Field(default="https://www.linkedin.com/jobs/", description="LinkedIn jobs URL")
    
    @classmethod
    def from_env(cls) -> "LinkedInConfig":
        """Create configuration from environment variables"""
        return cls(
            email=os.getenv("LINKEDIN_EMAIL", ""),
            password=os.getenv("LINKEDIN_PASSWORD", ""),
            job_keywords=os.getenv("JOB_KEYWORDS", "Data Analyst").split(","),
            easy_apply_only=os.getenv("EASY_APPLY_ONLY", "true").lower() == "true",
            max_applications_per_day=int(os.getenv("MAX_APPLICATIONS_PER_DAY", "10")),
            headless=os.getenv("HEADLESS", "false").lower() == "true",
            implicit_wait=int(os.getenv("IMPLICIT_WAIT", "10")),
            page_load_timeout=int(os.getenv("PAGE_LOAD_TIMEOUT", "30"))
        )


class JobApplicationConfig(BaseModel):
    """Configuration for job application settings"""
    
    # Application settings
    auto_apply: bool = Field(default=True, description="Automatically apply to jobs")
    send_messages: bool = Field(default=False, description="Send messages to recruiters")
    message_template: str = Field(
        default="Hello, I'm interested in this position and would love to learn more about the opportunity.",
        description="Default message template"
    )
    
    # Filtering criteria
    min_salary: Optional[int] = Field(default=None, description="Minimum salary requirement")
    experience_level: Optional[str] = Field(default=None, description="Experience level filter")
    location: Optional[str] = Field(default=None, description="Location filter")
    
    # Company preferences
    preferred_companies: list[str] = Field(default=[], description="List of preferred companies")
    blacklisted_companies: list[str] = Field(default=[], description="List of companies to avoid")


# Global configuration instance
config = LinkedInConfig.from_env()
job_config = JobApplicationConfig()
