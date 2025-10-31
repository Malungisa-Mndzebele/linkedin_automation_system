python3.13 -m pip install schedule"""
LinkedIn Job Application Automation - Web Application
Modern web UI for managing automatic job applications
"""
from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash
from flask_socketio import SocketIO, emit
import json
import os
import threading
import time
from datetime import datetime, timedelta
from typing import Dict, List, Any
import logging

from config import LinkedInConfig, JobApplicationConfig
from linkedin_automation import LinkedInAutomation
from comprehensive_logging import setup_comprehensive_logging
from database import DatabaseManager
from scheduler import AutomationScheduler

app = Flask(__name__)
app.config['SECRET_KEY'] = 'linkedin-automation-secret-key-2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Global variables for automation state
automation_instance = None
automation_thread = None
automation_running = False
automation_stats = {}
scheduler_instance = None

# Clear logs on startup
def clear_logs_on_startup():
    """Clear all log files on application startup"""
    import shutil
    import os
    
    log_dirs = ['logs', 'enhanced_logs']
    
    for log_dir in log_dirs:
        if os.path.exists(log_dir):
            try:
                shutil.rmtree(log_dir)
                print(f"✅ Cleared {log_dir} directory")
            except Exception as e:
                print(f"⚠️ Could not clear {log_dir}: {e}")
    
    # Recreate logs directory
    os.makedirs('logs', exist_ok=True)
    print("✅ Logs cleared and ready for new session")

# Clear logs on startup
clear_logs_on_startup()

# Initialize components
db_manager = DatabaseManager()
scheduler = AutomationScheduler()
comprehensive_logger = setup_comprehensive_logging("INFO")


class AutomationManager:
    """Manages the automation process and provides status updates"""
    
    def __init__(self):
        self.is_running = False
        self.current_config = None
        self.stats = {
            'jobs_found': 0,
            'applications_sent': 0,
            'success_rate': 0.0,
            'errors_count': 0,
            'session_duration': 0,
            'last_activity': None
        }
        self.logs = []
        
    def start_automation(self, config_data: Dict[str, Any]):
        """Start the automation process"""
        try:
            self.is_running = True
            self.current_config = config_data
            
            # Create configuration objects
            linkedin_config = LinkedInConfig(
                email=config_data['email'],
                password=config_data['password'],
                job_keywords=config_data['job_keywords'],
                easy_apply_only=config_data.get('easy_apply_only', True),
                max_applications_per_day=config_data.get('max_applications_per_day', 10),
                headless=config_data.get('headless', False),
                implicit_wait=10,
                page_load_timeout=30
            )
            
            job_config = JobApplicationConfig()
            
            # Initialize automation
            automation = LinkedInAutomation(linkedin_config, job_config)
            
            # Start automation in separate thread
            thread = threading.Thread(target=self._run_automation, args=(automation,))
            thread.daemon = True
            thread.start()
            
            return True
            
        except Exception as e:
            self.is_running = False
            comprehensive_logger.log_error("Automation Start", str(e), "Failed to start automation")
            return False
    
    def _run_automation(self, automation: LinkedInAutomation):
        """Run the automation process"""
        try:
            comprehensive_logger.log_session_start()
            
            # Start browser session
            if not automation.start_session():
                self._emit_error("Failed to start browser session")
                return
            
            # Login to LinkedIn
            if not automation.login():
                self._emit_error("Failed to login to LinkedIn")
                automation.close_session()
                return
            
            # Search for jobs
            if not automation.search_jobs():
                self._emit_error("Failed to search for jobs")
                automation.close_session()
                return
            
            # Get job listings
            jobs = automation.get_job_listings(max_jobs=20)
            self.stats['jobs_found'] = len(jobs)
            self._emit_update('jobs_found', len(jobs))
            
            if not jobs:
                self._emit_error("No job listings found")
                automation.close_session()
                return
            
            # Apply to jobs
            easy_apply_jobs = [job for job in jobs if job['has_easy_apply']]
            applications_sent = 0
            
            for i, job in enumerate(easy_apply_jobs, 1):
                if not self.is_running:
                    break
                    
                if applications_sent >= automation.config.max_applications_per_day:
                    self._emit_update('daily_limit_reached', True)
                    break
                
                self._emit_update('current_job', {
                    'title': job['title'],
                    'company': job['company'],
                    'number': i
                })
                
                if automation.apply_to_job(job):
                    applications_sent += 1
                    self.stats['applications_sent'] = applications_sent
                    self._emit_update('application_success', {
                        'title': job['title'],
                        'company': job['company'],
                        'total': applications_sent
                    })
                else:
                    self._emit_update('application_failed', {
                        'title': job['title'],
                        'company': job['company']
                    })
            
            # Calculate success rate
            if easy_apply_jobs:
                self.stats['success_rate'] = (applications_sent / len(easy_apply_jobs)) * 100
            
            # Close session
            automation.close_session()
            
            # Emit completion
            self._emit_update('automation_complete', self.stats)
            
        except Exception as e:
            self._emit_error(f"Automation failed: {str(e)}")
            comprehensive_logger.log_error("Automation Process", str(e), "Exception in automation thread")
        finally:
            self.is_running = False
            comprehensive_logger.log_session_end(self.stats)
    
    def stop_automation(self):
        """Stop the automation process"""
        self.is_running = False
        self._emit_update('automation_stopped', True)
    
    def _emit_update(self, event: str, data: Any):
        """Emit update to connected clients"""
        socketio.emit('automation_update', {
            'event': event,
            'data': data,
            'timestamp': datetime.now().isoformat()
        })
    
    def _emit_error(self, message: str):
        """Emit error to connected clients"""
        self.stats['errors_count'] += 1
        socketio.emit('automation_error', {
            'message': message,
            'timestamp': datetime.now().isoformat()
        })


# Initialize automation manager
automation_manager = AutomationManager()


@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('dashboard.html')


@app.route('/config')
def config_page():
    """Configuration page"""
    return render_template('config.html')


@app.route('/monitor')
def monitor_page():
    """Real-time monitoring page"""
    return render_template('monitor.html')


@app.route('/jobs')
def jobs_page():
    """Job management page"""
    return render_template('jobs.html')


@app.route('/logs')
def logs_page():
    """Logs and analytics page"""
    return render_template('logs.html')


@app.route('/api/config', methods=['GET', 'POST'])
def api_config():
    """API endpoint for configuration management"""
    if request.method == 'GET':
        # Return current configuration
        config_file = 'config.json'
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return jsonify(json.load(f))
        return jsonify({})
    
    elif request.method == 'POST':
        # Save configuration
        config_data = request.json
        
        # Validate required fields
        required_fields = ['email', 'password', 'job_keywords']
        for field in required_fields:
            if not config_data.get(field):
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Save to file
        with open('config.json', 'w') as f:
            json.dump(config_data, f, indent=2)
        
        return jsonify({'success': True, 'message': 'Configuration saved successfully'})


@app.route('/api/automation/start', methods=['POST'])
def api_start_automation():
    """API endpoint to start automation"""
    if automation_manager.is_running:
        return jsonify({'error': 'Automation is already running'}), 400
    
    config_data = request.json
    if not config_data:
        return jsonify({'error': 'No configuration provided'}), 400
    
    success = automation_manager.start_automation(config_data)
    
    if success:
        return jsonify({'success': True, 'message': 'Automation started successfully'})
    else:
        return jsonify({'error': 'Failed to start automation'}), 500


@app.route('/api/automation/stop', methods=['POST'])
def api_stop_automation():
    """API endpoint to stop automation"""
    automation_manager.stop_automation()
    return jsonify({'success': True, 'message': 'Automation stopped successfully'})


@app.route('/api/automation/status', methods=['GET'])
def api_automation_status():
    """API endpoint to get automation status"""
    return jsonify({
        'is_running': automation_manager.is_running,
        'stats': automation_manager.stats,
        'config': automation_manager.current_config
    })


@app.route('/api/jobs', methods=['GET'])
def api_jobs():
    """API endpoint to get job applications"""
    try:
        # Get job applications from database
        applications = db_manager.get_job_applications()
        return jsonify({'jobs': applications})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/logs', methods=['GET'])
def api_logs():
    """API endpoint to get recent logs"""
    try:
        logs_dir = 'logs'
        if not os.path.exists(logs_dir):
            return jsonify({'logs': []})
        
        # Get most recent log files
        log_files = []
        for filename in os.listdir(logs_dir):
            if filename.endswith('.log'):
                filepath = os.path.join(logs_dir, filename)
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                    log_files.append({
                        'filename': filename,
                        'content': content[-5000:],  # Last 5000 characters
                        'size': len(content)
                    })
        
        return jsonify({'logs': log_files})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def api_stats():
    """API endpoint to get statistics"""
    try:
        # Get statistics from database
        stats = db_manager.get_application_statistics()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@socketio.on('connect')
def handle_connect():
    """Handle client connection"""
    emit('connected', {'message': 'Connected to automation server'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection"""
    pass


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("Starting LinkedIn Automation Web Application...")
    print("Dashboard: http://localhost:5000")
    print("Configuration: http://localhost:5000/config")
    print("Monitoring: http://localhost:5000/monitor")
    print("Jobs: http://localhost:5000/jobs")
    print("Logs: http://localhost:5000/logs")
    
    socketio.run(app, debug=True, host='0.0.0.0', port=5000)
