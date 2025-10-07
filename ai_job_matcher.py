"""
AI-powered job matching and resume optimization
Uses machine learning to match jobs with user profile and optimize applications
"""
import re
import json
from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import logging
from datetime import datetime


@dataclass
class JobMatch:
    """Data class for job matching results"""
    job_id: str
    match_score: float
    reasons: List[str]
    missing_skills: List[str]
    recommended_actions: List[str]


@dataclass
class UserProfile:
    """Data class for user profile information"""
    skills: List[str]
    experience_years: int
    education: List[str]
    certifications: List[str]
    preferred_industries: List[str]
    preferred_locations: List[str]
    salary_expectation: Optional[int]
    remote_preference: bool
    company_size_preference: str  # startup, medium, large, enterprise


class AIJobMatcher:
    """AI-powered job matching and optimization"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.skill_keywords = self._load_skill_keywords()
        self.industry_keywords = self._load_industry_keywords()
        self.company_size_keywords = self._load_company_size_keywords()
    
    def _load_skill_keywords(self) -> Dict[str, List[str]]:
        """Load skill keywords for different categories"""
        return {
            'programming': [
                'python', 'java', 'javascript', 'typescript', 'c++', 'c#', 'go', 'rust',
                'php', 'ruby', 'swift', 'kotlin', 'scala', 'r', 'matlab', 'sql'
            ],
            'data_science': [
                'machine learning', 'deep learning', 'artificial intelligence', 'ai',
                'data analysis', 'statistics', 'pandas', 'numpy', 'scikit-learn',
                'tensorflow', 'pytorch', 'keras', 'spark', 'hadoop', 'tableau',
                'power bi', 'excel', 'r', 'python', 'sql'
            ],
            'web_development': [
                'html', 'css', 'javascript', 'react', 'angular', 'vue', 'node.js',
                'express', 'django', 'flask', 'spring', 'laravel', 'php', 'ruby on rails',
                'api', 'rest', 'graphql', 'microservices', 'docker', 'kubernetes'
            ],
            'cloud': [
                'aws', 'azure', 'gcp', 'google cloud', 'amazon web services',
                'docker', 'kubernetes', 'terraform', 'ansible', 'jenkins',
                'ci/cd', 'devops', 'microservices', 'serverless', 'lambda'
            ],
            'databases': [
                'mysql', 'postgresql', 'mongodb', 'redis', 'elasticsearch',
                'oracle', 'sql server', 'sqlite', 'cassandra', 'dynamodb'
            ],
            'soft_skills': [
                'leadership', 'communication', 'teamwork', 'problem solving',
                'project management', 'agile', 'scrum', 'mentoring', 'presentation'
            ]
        }
    
    def _load_industry_keywords(self) -> Dict[str, List[str]]:
        """Load industry-specific keywords"""
        return {
            'technology': ['software', 'tech', 'it', 'computer', 'digital', 'cyber'],
            'finance': ['banking', 'financial', 'fintech', 'investment', 'trading'],
            'healthcare': ['medical', 'health', 'pharmaceutical', 'biotech', 'clinical'],
            'retail': ['e-commerce', 'retail', 'consumer', 'shopping', 'marketplace'],
            'education': ['education', 'learning', 'training', 'academic', 'university'],
            'manufacturing': ['manufacturing', 'production', 'industrial', 'automation'],
            'consulting': ['consulting', 'advisory', 'strategy', 'management']
        }
    
    def _load_company_size_keywords(self) -> Dict[str, List[str]]:
        """Load company size indicators"""
        return {
            'startup': ['startup', 'early stage', 'seed', 'series a', 'small team'],
            'medium': ['mid-size', 'growing', 'established', 'medium'],
            'large': ['large', 'enterprise', 'fortune 500', 'multinational'],
            'enterprise': ['enterprise', 'fortune 500', 'global', 'multinational', 'corporate']
        }
    
    def extract_job_requirements(self, job_description: str) -> Dict[str, Any]:
        """Extract requirements and keywords from job description"""
        job_desc_lower = job_description.lower()
        
        # Extract skills
        found_skills = {}
        for category, skills in self.skill_keywords.items():
            found_skills[category] = []
            for skill in skills:
                if skill in job_desc_lower:
                    found_skills[category].append(skill)
        
        # Extract experience requirements
        experience_patterns = [
            r'(\d+)\+?\s*years?\s*(?:of\s*)?experience',
            r'(\d+)\+?\s*years?\s*in',
            r'minimum\s*(\d+)\s*years?',
            r'at\s*least\s*(\d+)\s*years?'
        ]
        
        experience_years = []
        for pattern in experience_patterns:
            matches = re.findall(pattern, job_desc_lower)
            experience_years.extend([int(match) for match in matches])
        
        min_experience = max(experience_years) if experience_years else 0
        
        # Extract education requirements
        education_keywords = ['bachelor', 'master', 'phd', 'degree', 'diploma', 'certification']
        education_required = [edu for edu in education_keywords if edu in job_desc_lower]
        
        # Extract location requirements
        location_patterns = [
            r'(?:in|at|located in)\s+([a-zA-Z\s,]+?)(?:\s|,|\.|$)',
            r'(?:based in|headquartered in)\s+([a-zA-Z\s,]+?)(?:\s|,|\.|$)'
        ]
        
        locations = []
        for pattern in location_patterns:
            matches = re.findall(pattern, job_desc_lower)
            locations.extend([match.strip() for match in matches])
        
        # Extract remote work indicators
        remote_indicators = ['remote', 'work from home', 'wfh', 'distributed', 'virtual']
        is_remote = any(indicator in job_desc_lower for indicator in remote_indicators)
        
        # Extract salary information
        salary_patterns = [
            r'\$(\d+(?:,\d{3})*(?:k|k\+)?)\s*(?:-|to|–)\s*\$(\d+(?:,\d{3})*(?:k|k\+)?)',
            r'salary[:\s]*\$(\d+(?:,\d{3})*(?:k|k\+)?)',
            r'compensation[:\s]*\$(\d+(?:,\d{3})*(?:k|k\+)?)'
        ]
        
        salary_range = None
        for pattern in salary_patterns:
            match = re.search(pattern, job_desc_lower)
            if match:
                salary_range = match.group(0)
                break
        
        return {
            'skills': found_skills,
            'min_experience': min_experience,
            'education_required': education_required,
            'locations': locations,
            'is_remote': is_remote,
            'salary_range': salary_range,
            'full_text': job_description
        }
    
    def calculate_match_score(self, user_profile: UserProfile, job_requirements: Dict[str, Any]) -> Tuple[float, List[str], List[str]]:
        """Calculate match score between user profile and job requirements"""
        reasons = []
        missing_skills = []
        
        # Skill matching (40% weight)
        skill_score = 0
        total_skills = 0
        
        for category, required_skills in job_requirements['skills'].items():
            if not required_skills:
                continue
            
            total_skills += len(required_skills)
            matched_skills = 0
            
            for skill in required_skills:
                if skill in [s.lower() for s in user_profile.skills]:
                    matched_skills += 1
                else:
                    missing_skills.append(skill)
            
            if matched_skills > 0:
                category_score = matched_skills / len(required_skills)
                skill_score += category_score * len(required_skills)
                reasons.append(f"Matched {matched_skills}/{len(required_skills)} {category} skills")
        
        skill_match_percentage = (skill_score / total_skills * 100) if total_skills > 0 else 0
        
        # Experience matching (25% weight)
        experience_score = 0
        if user_profile.experience_years >= job_requirements['min_experience']:
            experience_score = 100
            reasons.append(f"Meets experience requirement ({user_profile.experience_years} years)")
        else:
            experience_score = (user_profile.experience_years / job_requirements['min_experience'] * 100) if job_requirements['min_experience'] > 0 else 100
            reasons.append(f"Below experience requirement ({user_profile.experience_years}/{job_requirements['min_experience']} years)")
        
        # Education matching (15% weight)
        education_score = 0
        if not job_requirements['education_required']:
            education_score = 100
            reasons.append("No specific education requirements")
        else:
            user_education_lower = [edu.lower() for edu in user_profile.education]
            matched_education = any(req in ' '.join(user_education_lower) for req in job_requirements['education_required'])
            education_score = 100 if matched_education else 50
            if matched_education:
                reasons.append("Meets education requirements")
            else:
                reasons.append("May not meet education requirements")
        
        # Location matching (10% weight)
        location_score = 0
        if job_requirements['is_remote'] and user_profile.remote_preference:
            location_score = 100
            reasons.append("Remote work preference matched")
        elif not job_requirements['is_remote'] and user_profile.preferred_locations:
            # Check if any preferred location matches job locations
            job_locations_lower = [loc.lower() for loc in job_requirements['locations']]
            user_locations_lower = [loc.lower() for loc in user_profile.preferred_locations]
            location_match = any(user_loc in ' '.join(job_locations_lower) for user_loc in user_locations_lower)
            location_score = 100 if location_match else 50
            if location_match:
                reasons.append("Location preference matched")
            else:
                reasons.append("Location may not match preferences")
        else:
            location_score = 75  # Neutral score
        
        # Industry preference matching (10% weight)
        industry_score = 0
        if user_profile.preferred_industries:
            job_desc_lower = job_requirements['full_text'].lower()
            industry_match = any(industry in job_desc_lower for industry in user_profile.preferred_industries)
            industry_score = 100 if industry_match else 50
            if industry_match:
                reasons.append("Industry preference matched")
            else:
                reasons.append("Industry may not match preferences")
        else:
            industry_score = 75  # Neutral score
        
        # Calculate weighted total score
        total_score = (
            skill_match_percentage * 0.4 +
            experience_score * 0.25 +
            education_score * 0.15 +
            location_score * 0.1 +
            industry_score * 0.1
        )
        
        return round(total_score, 2), reasons, missing_skills
    
    def generate_recommendations(self, user_profile: UserProfile, job_requirements: Dict[str, Any], missing_skills: List[str]) -> List[str]:
        """Generate recommendations for improving job match"""
        recommendations = []
        
        # Skill recommendations
        if missing_skills:
            recommendations.append(f"Consider learning: {', '.join(missing_skills[:3])}")
        
        # Experience recommendations
        if user_profile.experience_years < job_requirements['min_experience']:
            years_needed = job_requirements['min_experience'] - user_profile.experience_years
            recommendations.append(f"Gain {years_needed} more years of experience or highlight relevant projects")
        
        # Education recommendations
        if job_requirements['education_required'] and not any(req in ' '.join([edu.lower() for edu in user_profile.education]) for req in job_requirements['education_required']):
            recommendations.append("Consider highlighting relevant certifications or equivalent experience")
        
        # Portfolio recommendations
        if any(category in ['programming', 'web_development', 'data_science'] for category in job_requirements['skills']):
            recommendations.append("Ensure your portfolio/GitHub profile is up to date")
        
        # Networking recommendations
        recommendations.append("Research the company and connect with current employees on LinkedIn")
        
        return recommendations
    
    def match_job(self, user_profile: UserProfile, job_title: str, job_description: str, company: str) -> JobMatch:
        """Main method to match a job with user profile"""
        job_requirements = self.extract_job_requirements(job_description)
        match_score, reasons, missing_skills = self.calculate_match_score(user_profile, job_requirements)
        recommendations = self.generate_recommendations(user_profile, job_requirements, missing_skills)
        
        # Generate job ID
        job_id = f"{company}_{job_title}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        return JobMatch(
            job_id=job_id,
            match_score=match_score,
            reasons=reasons,
            missing_skills=missing_skills,
            recommended_actions=recommendations
        )
    
    def optimize_resume_keywords(self, user_profile: UserProfile, job_description: str) -> List[str]:
        """Suggest keywords to add to resume for better ATS matching"""
        job_requirements = self.extract_job_requirements(job_description)
        suggested_keywords = []
        
        # Extract important keywords from job description
        important_keywords = []
        for category, skills in job_requirements['skills'].items():
            important_keywords.extend(skills)
        
        # Find missing keywords that user should add
        user_skills_lower = [skill.lower() for skill in user_profile.skills]
        missing_keywords = [keyword for keyword in important_keywords if keyword not in user_skills_lower]
        
        # Prioritize by frequency in job description
        job_desc_lower = job_description.lower()
        keyword_frequency = {}
        for keyword in missing_keywords:
            keyword_frequency[keyword] = job_desc_lower.count(keyword)
        
        # Return top 5 most frequent missing keywords
        sorted_keywords = sorted(keyword_frequency.items(), key=lambda x: x[1], reverse=True)
        suggested_keywords = [keyword for keyword, freq in sorted_keywords[:5]]
        
        return suggested_keywords
