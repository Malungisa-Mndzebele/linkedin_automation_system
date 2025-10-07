"""
Database management for LinkedIn Job Application Automation
Handles application tracking, job history, and analytics
"""
import sqlite3
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import logging


@dataclass
class JobApplication:
    """Data class for job application records"""
    id: Optional[int] = None
    job_title: str = ""
    company: str = ""
    job_url: str = ""
    application_date: datetime = None
    status: str = "applied"  # applied, interviewed, rejected, accepted
    easy_apply: bool = False
    notes: str = ""
    salary_range: str = ""
    location: str = ""
    job_description: str = ""
    response_received: bool = False
    response_date: Optional[datetime] = None
    interview_scheduled: bool = False
    interview_date: Optional[datetime] = None


@dataclass
class JobSearch:
    """Data class for job search sessions"""
    id: Optional[int] = None
    search_date: datetime = None
    keywords: str = ""
    location: str = ""
    jobs_found: int = 0
    applications_sent: int = 0
    success_rate: float = 0.0
    session_duration: int = 0  # in minutes


class DatabaseManager:
    """Manages SQLite database for application tracking"""
    
    def __init__(self, db_path: str = "linkedin_automation.db"):
        self.db_path = db_path
        self.logger = logging.getLogger(__name__)
        self._init_database()
    
    def _init_database(self):
        """Initialize database tables"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Job applications table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_applications (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    job_title TEXT NOT NULL,
                    company TEXT NOT NULL,
                    job_url TEXT,
                    application_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    status TEXT DEFAULT 'applied',
                    easy_apply BOOLEAN DEFAULT FALSE,
                    notes TEXT,
                    salary_range TEXT,
                    location TEXT,
                    job_description TEXT,
                    response_received BOOLEAN DEFAULT FALSE,
                    response_date TIMESTAMP,
                    interview_scheduled BOOLEAN DEFAULT FALSE,
                    interview_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Job search sessions table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS job_search_sessions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    search_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    keywords TEXT NOT NULL,
                    location TEXT,
                    jobs_found INTEGER DEFAULT 0,
                    applications_sent INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    session_duration INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # User profiles table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS user_profiles (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    profile_name TEXT,
                    is_active BOOLEAN DEFAULT TRUE,
                    daily_application_limit INTEGER DEFAULT 10,
                    preferred_keywords TEXT,
                    preferred_companies TEXT,
                    blacklisted_companies TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Analytics table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS analytics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    date DATE NOT NULL,
                    total_applications INTEGER DEFAULT 0,
                    total_interviews INTEGER DEFAULT 0,
                    total_offers INTEGER DEFAULT 0,
                    success_rate REAL DEFAULT 0.0,
                    avg_response_time INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            conn.commit()
            self.logger.info("Database initialized successfully")
    
    def add_job_application(self, application: JobApplication) -> int:
        """Add a new job application record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO job_applications 
                (job_title, company, job_url, application_date, status, easy_apply, 
                 notes, salary_range, location, job_description, response_received, 
                 response_date, interview_scheduled, interview_date)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                application.job_title, application.company, application.job_url,
                application.application_date or datetime.now(), application.status,
                application.easy_apply, application.notes, application.salary_range,
                application.location, application.job_description, application.response_received,
                application.response_date, application.interview_scheduled, application.interview_date
            ))
            conn.commit()
            return cursor.lastrowid
    
    def update_job_application(self, application_id: int, updates: Dict[str, Any]):
        """Update an existing job application"""
        set_clause = ", ".join([f"{key} = ?" for key in updates.keys()])
        updates['updated_at'] = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute(f"""
                UPDATE job_applications 
                SET {set_clause}, updated_at = ?
                WHERE id = ?
            """, list(updates.values()) + [application_id])
            conn.commit()
    
    def get_job_applications(self, limit: int = 100, status: Optional[str] = None) -> List[JobApplication]:
        """Get job applications with optional filtering"""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            query = "SELECT * FROM job_applications"
            params = []
            
            if status:
                query += " WHERE status = ?"
                params.append(status)
            
            query += " ORDER BY application_date DESC LIMIT ?"
            params.append(limit)
            
            cursor.execute(query, params)
            rows = cursor.fetchall()
            
            applications = []
            for row in rows:
                app = JobApplication(
                    id=row['id'],
                    job_title=row['job_title'],
                    company=row['company'],
                    job_url=row['job_url'],
                    application_date=datetime.fromisoformat(row['application_date']) if row['application_date'] else None,
                    status=row['status'],
                    easy_apply=bool(row['easy_apply']),
                    notes=row['notes'] or "",
                    salary_range=row['salary_range'] or "",
                    location=row['location'] or "",
                    job_description=row['job_description'] or "",
                    response_received=bool(row['response_received']),
                    response_date=datetime.fromisoformat(row['response_date']) if row['response_date'] else None,
                    interview_scheduled=bool(row['interview_scheduled']),
                    interview_date=datetime.fromisoformat(row['interview_date']) if row['interview_date'] else None
                )
                applications.append(app)
            
            return applications
    
    def add_job_search_session(self, session: JobSearch) -> int:
        """Add a new job search session record"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO job_search_sessions 
                (search_date, keywords, location, jobs_found, applications_sent, 
                 success_rate, session_duration)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session.search_date or datetime.now(), session.keywords, session.location,
                session.jobs_found, session.applications_sent, session.success_rate,
                session.session_duration
            ))
            conn.commit()
            return cursor.lastrowid
    
    def get_analytics(self, days: int = 30) -> Dict[str, Any]:
        """Get analytics data for the specified number of days"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Get date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            # Total applications
            cursor.execute("""
                SELECT COUNT(*) FROM job_applications 
                WHERE application_date >= ? AND application_date <= ?
            """, (start_date, end_date))
            total_applications = cursor.fetchone()[0]
            
            # Applications by status
            cursor.execute("""
                SELECT status, COUNT(*) FROM job_applications 
                WHERE application_date >= ? AND application_date <= ?
                GROUP BY status
            """, (start_date, end_date))
            status_counts = dict(cursor.fetchall())
            
            # Daily application counts
            cursor.execute("""
                SELECT DATE(application_date) as date, COUNT(*) as count
                FROM job_applications 
                WHERE application_date >= ? AND application_date <= ?
                GROUP BY DATE(application_date)
                ORDER BY date
            """, (start_date, end_date))
            daily_counts = cursor.fetchall()
            
            # Success rate
            total_responses = status_counts.get('interviewed', 0) + status_counts.get('accepted', 0)
            success_rate = (total_responses / total_applications * 100) if total_applications > 0 else 0
            
            # Top companies
            cursor.execute("""
                SELECT company, COUNT(*) as count
                FROM job_applications 
                WHERE application_date >= ? AND application_date <= ?
                GROUP BY company
                ORDER BY count DESC
                LIMIT 10
            """, (start_date, end_date))
            top_companies = cursor.fetchall()
            
            return {
                'total_applications': total_applications,
                'status_breakdown': status_counts,
                'success_rate': round(success_rate, 2),
                'daily_counts': daily_counts,
                'top_companies': top_companies,
                'date_range': {
                    'start': start_date.strftime('%Y-%m-%d'),
                    'end': end_date.strftime('%Y-%m-%d')
                }
            }
    
    def get_daily_stats(self, date: Optional[datetime] = None) -> Dict[str, Any]:
        """Get statistics for a specific day"""
        if date is None:
            date = datetime.now()
        
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            # Applications for the day
            cursor.execute("""
                SELECT COUNT(*) FROM job_applications 
                WHERE DATE(application_date) = DATE(?)
            """, (date,))
            daily_applications = cursor.fetchone()[0]
            
            # Remaining applications (based on limit)
            cursor.execute("""
                SELECT daily_application_limit FROM user_profiles 
                WHERE is_active = TRUE LIMIT 1
            """)
            result = cursor.fetchone()
            daily_limit = result[0] if result else 10
            remaining_applications = max(0, daily_limit - daily_applications)
            
            return {
                'date': date.strftime('%Y-%m-%d'),
                'applications_sent': daily_applications,
                'daily_limit': daily_limit,
                'remaining_applications': remaining_applications,
                'can_apply': remaining_applications > 0
            }
    
    def close(self):
        """Close database connection"""
        pass  # SQLite connections are closed automatically
