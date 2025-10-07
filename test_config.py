"""
Unit tests for configuration management
"""
import pytest
import os
from unittest.mock import patch
from config import LinkedInConfig, JobApplicationConfig


class TestLinkedInConfig:
    """Test cases for LinkedInConfig class"""
    
    def test_config_creation_with_defaults(self):
        """Test creating config with default values"""
        config = LinkedInConfig(
            email="test@example.com",
            password="testpassword"
        )
        
        assert config.email == "test@example.com"
        assert config.password == "testpassword"
        assert config.job_keywords == ["Data Analyst"]
        assert config.easy_apply_only is True
        assert config.max_applications_per_day == 10
        assert config.headless is False
        assert config.implicit_wait == 10
        assert config.page_load_timeout == 30
    
    def test_config_creation_with_custom_values(self):
        """Test creating config with custom values"""
        config = LinkedInConfig(
            email="custom@example.com",
            password="custompassword",
            job_keywords=["Data Scientist", "ML Engineer"],
            easy_apply_only=False,
            max_applications_per_day=20,
            headless=True,
            implicit_wait=15,
            page_load_timeout=45
        )
        
        assert config.email == "custom@example.com"
        assert config.password == "custompassword"
        assert config.job_keywords == ["Data Scientist", "ML Engineer"]
        assert config.easy_apply_only is False
        assert config.max_applications_per_day == 20
        assert config.headless is True
        assert config.implicit_wait == 15
        assert config.page_load_timeout == 45
    
    @patch.dict(os.environ, {
        'LINKEDIN_EMAIL': 'env@example.com',
        'LINKEDIN_PASSWORD': 'envpassword',
        'JOB_KEYWORDS': 'Data Analyst,Business Analyst',
        'EASY_APPLY_ONLY': 'false',
        'MAX_APPLICATIONS_PER_DAY': '15',
        'HEADLESS': 'true',
        'IMPLICIT_WAIT': '20',
        'PAGE_LOAD_TIMEOUT': '60'
    })
    def test_config_from_env(self):
        """Test creating config from environment variables"""
        config = LinkedInConfig.from_env()
        
        assert config.email == "env@example.com"
        assert config.password == "envpassword"
        assert config.job_keywords == ["Data Analyst", "Business Analyst"]
        assert config.easy_apply_only is False
        assert config.max_applications_per_day == 15
        assert config.headless is True
        assert config.implicit_wait == 20
        assert config.page_load_timeout == 60
    
    @patch.dict(os.environ, {}, clear=True)
    def test_config_from_env_with_defaults(self):
        """Test creating config from environment with missing variables"""
        config = LinkedInConfig.from_env()
        
        assert config.email == ""
        assert config.password == ""
        assert config.job_keywords == ["Data Analyst"]
        assert config.easy_apply_only is True
        assert config.max_applications_per_day == 10
        assert config.headless is False
        assert config.implicit_wait == 10
        assert config.page_load_timeout == 30
    
    def test_config_validation(self):
        """Test config validation with invalid values"""
        # Test with empty email (should work as Pydantic allows empty strings by default)
        config1 = LinkedInConfig(
            email="",  # Empty email
            password="testpassword"
        )
        assert config1.email == ""
        
        # Test with empty password (should work as Pydantic allows empty strings by default)
        config2 = LinkedInConfig(
            email="test@example.com",
            password=""  # Empty password
        )
        assert config2.password == ""


class TestJobApplicationConfig:
    """Test cases for JobApplicationConfig class"""
    
    def test_job_config_creation_with_defaults(self):
        """Test creating job config with default values"""
        config = JobApplicationConfig()
        
        assert config.auto_apply is True
        assert config.send_messages is False
        assert "interested in this position" in config.message_template
        assert config.min_salary is None
        assert config.experience_level is None
        assert config.location is None
        assert config.preferred_companies == []
        assert config.blacklisted_companies == []
    
    def test_job_config_creation_with_custom_values(self):
        """Test creating job config with custom values"""
        config = JobApplicationConfig(
            auto_apply=False,
            send_messages=True,
            message_template="Custom message template",
            min_salary=50000,
            experience_level="Mid-level",
            location="Remote",
            preferred_companies=["Google", "Microsoft"],
            blacklisted_companies=["Company A", "Company B"]
        )
        
        assert config.auto_apply is False
        assert config.send_messages is True
        assert config.message_template == "Custom message template"
        assert config.min_salary == 50000
        assert config.experience_level == "Mid-level"
        assert config.location == "Remote"
        assert config.preferred_companies == ["Google", "Microsoft"]
        assert config.blacklisted_companies == ["Company A", "Company B"]
    
    def test_job_config_validation(self):
        """Test job config validation"""
        # Test with valid values
        config = JobApplicationConfig(
            min_salary=0,  # Should be valid
            experience_level="",  # Empty string should be valid
            location="   "  # Whitespace should be valid
        )
        
        assert config.min_salary == 0
        assert config.experience_level == ""
        assert config.location == "   "
