"""
Simple Scheduler for LinkedIn Job Application Automation
Basic version without external dependencies
"""
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
import logging


class SimpleScheduler:
    """Simple scheduler for automation timing"""
    
    def __init__(self, config_file: str = "scheduler_config.json"):
        self.config_file = config_file
        self.logger = logging.getLogger(__name__)
        self.config = self._load_config()
        self.daily_stats = self._load_daily_stats()
    
    def _load_config(self) -> Dict[str, Any]:
        """Load scheduler configuration"""
        default_config = {
            "enabled": True,
            "daily_application_limit": 10,
            "optimal_times": {
                "morning": {"start": "09:00", "end": "11:00"},
                "afternoon": {"start": "14:00", "end": "16:00"},
                "evening": {"start": "19:00", "end": "21:00"}
            },
            "weekdays_only": True,
            "avoid_weekends": True,
            "timezone": "UTC",
            "random_delay_min": 30,
            "random_delay_max": 300,
            "cooldown_between_applications": 60,
            "max_session_duration": 120,
            "auto_pause_on_limit": True,
            "resume_next_day": True
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r') as f:
                    config = json.load(f)
                # Merge with defaults for any missing keys
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                return config
            except Exception as e:
                self.logger.warning(f"Failed to load config: {e}. Using defaults.")
        
        return default_config
    
    def _load_daily_stats(self) -> Dict[str, Any]:
        """Load daily statistics"""
        stats_file = "daily_stats.json"
        default_stats = {
            "current_date": datetime.now().strftime('%Y-%m-%d'),
            "applications_sent": 0,
            "last_application_time": None,
            "session_start_time": None,
            "total_session_time": 0,
            "paused_until": None
        }
        
        if os.path.exists(stats_file):
            try:
                with open(stats_file, 'r') as f:
                    stats = json.load(f)
                # Reset if it's a new day
                if stats.get("current_date") != datetime.now().strftime('%Y-%m-%d'):
                    stats = default_stats
                    stats["current_date"] = datetime.now().strftime('%Y-%m-%d')
                return stats
            except Exception as e:
                self.logger.warning(f"Failed to load daily stats: {e}")
        
        return default_stats
    
    def can_apply_now(self) -> tuple[bool, str]:
        """Check if automation can run now"""
        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')
        
        # Check if it's a new day
        if self.daily_stats.get("current_date") != current_date:
            self._reset_daily_stats()
        
        # Check if paused
        if self.daily_stats.get("paused_until"):
            pause_until = datetime.fromisoformat(self.daily_stats["paused_until"])
            if current_time < pause_until:
                return False, f"Automation paused until {pause_until.strftime('%H:%M:%S')}"
        
        # Check daily limit
        if self.daily_stats["applications_sent"] >= self.config["daily_application_limit"]:
            if self.config["auto_pause_on_limit"]:
                return False, "Daily application limit reached"
            else:
                return True, "Daily limit reached but auto-pause disabled"
        
        # Check if it's a good time to apply
        if not self._is_optimal_time():
            return False, "Not an optimal time for applications"
        
        # Check weekday restriction
        if self.config["weekdays_only"] and current_time.weekday() >= 5:  # Saturday = 5, Sunday = 6
            return False, "Weekend - automation disabled"
        
        return True, "Ready to apply"
    
    def _is_optimal_time(self) -> bool:
        """Check if current time is optimal for applications"""
        current_time = datetime.now().time()
        
        for period, times in self.config["optimal_times"].items():
            start_time = datetime.strptime(times["start"], "%H:%M").time()
            end_time = datetime.strptime(times["end"], "%H:%M").time()
            
            if start_time <= current_time <= end_time:
                return True
        
        return False
    
    def _reset_daily_stats(self):
        """Reset daily statistics for a new day"""
        self.daily_stats = {
            "current_date": datetime.now().strftime('%Y-%m-%d'),
            "applications_sent": 0,
            "last_application_time": None,
            "session_start_time": None,
            "total_session_time": 0,
            "paused_until": None
        }
        self._save_daily_stats()
        self.logger.info("Daily stats reset for new day")
    
    def _save_daily_stats(self):
        """Save daily statistics"""
        stats_file = "daily_stats.json"
        try:
            with open(stats_file, 'w') as f:
                json.dump(self.daily_stats, f, indent=2)
        except Exception as e:
            self.logger.error(f"Failed to save daily stats: {e}")
    
    def record_application(self):
        """Record that an application was sent"""
        current_time = datetime.now()
        self.daily_stats["applications_sent"] += 1
        self.daily_stats["last_application_time"] = current_time.isoformat()
        
        # Start session if not already started
        if not self.daily_stats.get("session_start_time"):
            self.daily_stats["session_start_time"] = current_time.isoformat()
        
        self._save_daily_stats()
        self.logger.info(f"Application recorded. Total today: {self.daily_stats['applications_sent']}")
    
    def get_daily_progress(self) -> Dict[str, Any]:
        """Get daily progress information"""
        can_apply, reason = self.can_apply_now()
        next_optimal = self.get_next_optimal_time()
        
        return {
            "applications_sent": self.daily_stats["applications_sent"],
            "daily_limit": self.config["daily_application_limit"],
            "remaining_applications": max(0, self.config["daily_application_limit"] - self.daily_stats["applications_sent"]),
            "can_apply_now": can_apply,
            "reason": reason,
            "next_optimal_time": next_optimal.isoformat() if next_optimal else None,
            "is_paused": bool(self.daily_stats.get("paused_until")),
            "paused_until": self.daily_stats.get("paused_until")
        }
    
    def get_next_optimal_time(self) -> Optional[datetime]:
        """Get the next optimal time for applications"""
        current_time = datetime.now()
        current_date = current_time.date()
        
        # Check today's remaining optimal times
        for period, times in self.config["optimal_times"].items():
            start_time = datetime.strptime(times["start"], "%H:%M").time()
            end_time = datetime.strptime(times["end"], "%H:%M").time()
            
            # Create datetime objects for today
            start_datetime = datetime.combine(current_date, start_time)
            end_datetime = datetime.combine(current_date, end_time)
            
            # If current time is before this period, return start time
            if current_time < start_datetime:
                return start_datetime
            
            # If current time is within this period, return current time
            if start_datetime <= current_time <= end_datetime:
                return current_time
        
        # If no optimal time today, return first optimal time tomorrow
        tomorrow = current_date + timedelta(days=1)
        first_period = min(self.config["optimal_times"].items(), 
                          key=lambda x: x[1]["start"])
        start_time = datetime.strptime(first_period[1]["start"], "%H:%M").time()
        return datetime.combine(tomorrow, start_time)
    
    def pause_automation(self, duration_minutes: int = 60):
        """Pause automation for specified duration"""
        pause_until = datetime.now() + timedelta(minutes=duration_minutes)
        self.daily_stats["paused_until"] = pause_until.isoformat()
        self._save_daily_stats()
        self.logger.info(f"Automation paused until {pause_until.strftime('%H:%M:%S')}")
    
    def resume_automation(self):
        """Resume automation"""
        self.daily_stats["paused_until"] = None
        self._save_daily_stats()
        self.logger.info("Automation resumed")
    
    def get_config(self) -> Dict[str, Any]:
        """Get current scheduler configuration"""
        return self.config.copy()
    
    def update_config(self, new_config: Dict[str, Any]):
        """Update scheduler configuration"""
        self.config.update(new_config)
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.config, f, indent=2)
            self.logger.info("Scheduler configuration updated")
        except Exception as e:
            self.logger.error(f"Failed to save config: {e}")
