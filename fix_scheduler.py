"""
Quick fix for scheduler to allow applications at any time
"""
import json
from datetime import datetime

def fix_scheduler_config():
    """Update scheduler config to allow applications at any time"""
    
    # Load current config
    with open('scheduler_config.json', 'r') as f:
        config = json.load(f)
    
    # Update optimal times to allow applications throughout the day
    config['optimal_times'] = {
        "all_day": {
            "start": "08:00",
            "end": "22:00"
        }
    }
    
    # Save updated config
    with open('scheduler_config.json', 'w') as f:
        json.dump(config, f, indent=2)
    
    print("Scheduler configuration updated to allow applications from 8:00 AM to 10:00 PM")
    print("Current time:", datetime.now().strftime("%H:%M:%S"))

if __name__ == "__main__":
    fix_scheduler_config()
