"""
Configuration management for LinkedIn Job Application Automation MVP
"""
import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


# Try to import pydantic, but provide a lightweight dataclass fallback so tests
# and lightweight scripts can run without building pydantic-core (which may
# require compilation tools on some systems).
try:
    from pydantic import BaseModel, Field

    class LinkedInConfig(BaseModel):
        """Configuration model for LinkedIn automation (pydantic)
        """
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
        job_search_timeout: int = Field(default=30, description="Job search results timeout in seconds")
        element_wait_timeout: int = Field(default=15, description="Element wait timeout in seconds")

        # URLs
        linkedin_login_url: str = Field(default="https://www.linkedin.com/login", description="LinkedIn login URL")
        linkedin_jobs_url: str = Field(default="https://www.linkedin.com/jobs/", description="LinkedIn jobs URL")

        @classmethod
        def from_env(cls) -> "LinkedInConfig":
            return cls(
                email=os.getenv("LINKEDIN_EMAIL", ""),
                password=os.getenv("LINKEDIN_PASSWORD", ""),
                job_keywords=os.getenv("JOB_KEYWORDS", "Data Analyst").split(","),
                easy_apply_only=os.getenv("EASY_APPLY_ONLY", "true").lower() == "true",
                max_applications_per_day=int(os.getenv("MAX_APPLICATIONS_PER_DAY", "10")),
                headless=os.getenv("HEADLESS", "false").lower() == "true",
                implicit_wait=int(os.getenv("IMPLICIT_WAIT", "10")),
                page_load_timeout=int(os.getenv("PAGE_LOAD_TIMEOUT", "30")),
            )


    class JobApplicationConfig(BaseModel):
        """Configuration for job application settings (pydantic)
        """
        auto_apply: bool = Field(default=True, description="Automatically apply to jobs")
        send_messages: bool = Field(default=False, description="Send messages to recruiters")
        message_template: str = Field(
            default="Hello, I'm interested in this position and would love to learn more about the opportunity.",
            description="Default message template",
        )

        min_salary: Optional[int] = Field(default=None, description="Minimum salary requirement")
        experience_level: Optional[str] = Field(default=None, description="Experience level filter")
        location: Optional[str] = Field(default=None, description="Location filter")

        preferred_companies: list[str] = Field(default=[], description="List of preferred companies")
        blacklisted_companies: list[str] = Field(default=[], description="List of companies to avoid")

except Exception:
    # Lightweight fallback for environments without pydantic
    from dataclasses import dataclass, field


    @dataclass
    class LinkedInConfig:
        email: str
        password: str
        job_keywords: list[str] = field(default_factory=lambda: ["Data Analyst"])
        easy_apply_only: bool = True
        max_applications_per_day: int = 10
        headless: bool = False
        implicit_wait: int = 10
        page_load_timeout: int = 30
        job_search_timeout: int = 30
        element_wait_timeout: int = 15
        linkedin_login_url: str = "https://www.linkedin.com/login"
        linkedin_jobs_url: str = "https://www.linkedin.com/jobs/"

        @classmethod
        def from_env(cls) -> "LinkedInConfig":
            return cls(
                email=os.getenv("LINKEDIN_EMAIL", ""),
                password=os.getenv("LINKEDIN_PASSWORD", ""),
                job_keywords=os.getenv("JOB_KEYWORDS", "Data Analyst").split(","),
                easy_apply_only=os.getenv("EASY_APPLY_ONLY", "true").lower() == "true",
                max_applications_per_day=int(os.getenv("MAX_APPLICATIONS_PER_DAY", "10")),
                headless=os.getenv("HEADLESS", "false").lower() == "true",
                implicit_wait=int(os.getenv("IMPLICIT_WAIT", "10")),
                page_load_timeout=int(os.getenv("PAGE_LOAD_TIMEOUT", "30")),
            )


    @dataclass
    class JobApplicationConfig:
        auto_apply: bool = True
        send_messages: bool = False
        message_template: str = "Hello, I'm interested in this position and would love to learn more about the opportunity."
        min_salary: Optional[int] = None
        experience_level: Optional[str] = None
        location: Optional[str] = None
        preferred_companies: list[str] = field(default_factory=list)
        blacklisted_companies: list[str] = field(default_factory=list)


# Global configuration instance
config = LinkedInConfig.from_env()
job_config = JobApplicationConfig()
