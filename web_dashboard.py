"""
Web dashboard for LinkedIn Job Application Automation
Provides real-time monitoring, control, and analytics
"""
from flask import Flask, render_template, jsonify, request, redirect, url_for
import json
import os
from datetime import datetime, timedelta
from typing import Dict, Any, List
import logging
from database import DatabaseManager
from scheduler import AutomationScheduler
import threading
import time


class WebDashboard:
    """Web dashboard for automation monitoring and control"""
    
    def __init__(self, host='127.0.0.1', port=5000, debug=False):
        self.app = Flask(__name__)
        self.app.secret_key = 'linkedin_automation_secret_key'
        self.host = host
        self.port = port
        self.debug = debug
        self.logger = logging.getLogger(__name__)
        
        # Initialize components
        self.db_manager = DatabaseManager()
        self.scheduler = AutomationScheduler()
        
        # Dashboard state
        self.automation_status = {
            'is_running': False,
            'current_job': None,
            'last_activity': None,
            'error_count': 0,
            'success_count': 0
        }
        
        self._setup_routes()
        self._start_background_tasks()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page"""
            return render_template('dashboard.html')
        
        @self.app.route('/api/status')
        def api_status():
            """Get automation status"""
            return jsonify({
                'automation': self.automation_status,
                'scheduler': self.scheduler.get_daily_progress(),
                'timestamp': datetime.now().isoformat()
            })
        
        @self.app.route('/api/analytics')
        def api_analytics():
            """Get analytics data"""
            days = request.args.get('days', 30, type=int)
            analytics = self.db_manager.get_analytics(days)
            return jsonify(analytics)
        
        @self.app.route('/api/applications')
        def api_applications():
            """Get job applications"""
            limit = request.args.get('limit', 50, type=int)
            status = request.args.get('status', None)
            applications = self.db_manager.get_job_applications(limit, status)
            
            # Convert to JSON-serializable format
            apps_data = []
            for app in applications:
                app_data = {
                    'id': app.id,
                    'job_title': app.job_title,
                    'company': app.company,
                    'job_url': app.job_url,
                    'application_date': app.application_date.isoformat() if app.application_date else None,
                    'status': app.status,
                    'easy_apply': app.easy_apply,
                    'notes': app.notes,
                    'salary_range': app.salary_range,
                    'location': app.location,
                    'response_received': app.response_received,
                    'interview_scheduled': app.interview_scheduled
                }
                apps_data.append(app_data)
            
            return jsonify(apps_data)
        
        @self.app.route('/api/control/start', methods=['POST'])
        def api_start_automation():
            """Start automation"""
            try:
                # This would integrate with the main automation system
                self.automation_status['is_running'] = True
                self.automation_status['last_activity'] = datetime.now().isoformat()
                return jsonify({'success': True, 'message': 'Automation started'})
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)}), 500
        
        @self.app.route('/api/control/stop', methods=['POST'])
        def api_stop_automation():
            """Stop automation"""
            try:
                self.automation_status['is_running'] = False
                self.automation_status['last_activity'] = datetime.now().isoformat()
                return jsonify({'success': True, 'message': 'Automation stopped'})
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)}), 500
        
        @self.app.route('/api/control/pause', methods=['POST'])
        def api_pause_automation():
            """Pause automation"""
            try:
                duration = request.json.get('duration', 60)
                self.scheduler.pause_automation(duration)
                return jsonify({'success': True, 'message': f'Automation paused for {duration} minutes'})
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)}), 500
        
        @self.app.route('/api/control/resume', methods=['POST'])
        def api_resume_automation():
            """Resume automation"""
            try:
                self.scheduler.resume_automation()
                return jsonify({'success': True, 'message': 'Automation resumed'})
            except Exception as e:
                return jsonify({'success': False, 'message': str(e)}), 500
        
        @self.app.route('/api/config', methods=['GET', 'POST'])
        def api_config():
            """Get or update configuration"""
            if request.method == 'GET':
                return jsonify(self.scheduler.get_config())
            else:
                try:
                    new_config = request.json
                    self.scheduler.update_config(new_config)
                    return jsonify({'success': True, 'message': 'Configuration updated'})
                except Exception as e:
                    return jsonify({'success': False, 'message': str(e)}), 500
        
        @self.app.route('/api/logs')
        def api_logs():
            """Get recent logs"""
            try:
                log_file = 'linkedin_automation.log'
                if not os.path.exists(log_file):
                    return jsonify([])
                
                # Read last 100 lines
                with open(log_file, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    recent_lines = lines[-100:] if len(lines) > 100 else lines
                
                logs = []
                for line in recent_lines:
                    if line.strip():
                        # Parse log line (basic parsing)
                        parts = line.split(' - ', 3)
                        if len(parts) >= 4:
                            timestamp = parts[0]
                            level = parts[1]
                            logger_name = parts[2]
                            message = parts[3].strip()
                            
                            logs.append({
                                'timestamp': timestamp,
                                'level': level,
                                'logger': logger_name,
                                'message': message
                            })
                
                return jsonify(logs)
            except Exception as e:
                return jsonify({'error': str(e)}), 500
    
    def _start_background_tasks(self):
        """Start background tasks for real-time updates"""
        def update_status():
            while True:
                try:
                    # Update automation status
                    if self.automation_status['is_running']:
                        # Check if automation is still running (this would integrate with actual automation)
                        pass
                    
                    time.sleep(30)  # Update every 30 seconds
                except Exception as e:
                    self.logger.error(f"Background task error: {e}")
                    time.sleep(60)
        
        # Start background thread
        background_thread = threading.Thread(target=update_status, daemon=True)
        background_thread.start()
    
    def run(self):
        """Run the web dashboard"""
        self.logger.info(f"Starting web dashboard on {self.host}:{self.port}")
        self.app.run(host=self.host, port=self.port, debug=self.debug, threaded=True)


# Create templates directory and HTML files
def create_dashboard_templates():
    """Create HTML templates for the dashboard"""
    templates_dir = "templates"
    os.makedirs(templates_dir, exist_ok=True)
    
    # Main dashboard template
    dashboard_html = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>LinkedIn Automation Dashboard</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        .status-card { transition: all 0.3s ease; }
        .status-card:hover { transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,0,0,0.1); }
        .metric-value { font-size: 2rem; font-weight: bold; }
        .metric-label { color: #6c757d; }
        .status-running { color: #28a745; }
        .status-stopped { color: #dc3545; }
        .status-paused { color: #ffc107; }
    </style>
</head>
<body>
    <nav class="navbar navbar-dark bg-dark">
        <div class="container-fluid">
            <span class="navbar-brand mb-0 h1">
                <i class="fab fa-linkedin"></i> LinkedIn Automation Dashboard
            </span>
            <span class="navbar-text" id="last-update">
                Last updated: <span id="update-time">--</span>
            </span>
        </div>
    </nav>

    <div class="container-fluid mt-4">
        <!-- Status Cards -->
        <div class="row mb-4">
            <div class="col-md-3">
                <div class="card status-card">
                    <div class="card-body text-center">
                        <i class="fas fa-play-circle fa-2x mb-2" id="status-icon"></i>
                        <h5 class="card-title">Status</h5>
                        <p class="card-text" id="status-text">Stopped</p>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card status-card">
                    <div class="card-body text-center">
                        <div class="metric-value" id="daily-applications">0</div>
                        <div class="metric-label">Applications Today</div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card status-card">
                    <div class="card-body text-center">
                        <div class="metric-value" id="remaining-applications">0</div>
                        <div class="metric-label">Remaining</div>
                    </div>
                </div>
            </div>
            <div class="col-md-3">
                <div class="card status-card">
                    <div class="card-body text-center">
                        <div class="metric-value" id="success-rate">0%</div>
                        <div class="metric-label">Success Rate</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Control Panel -->
        <div class="row mb-4">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-cogs"></i> Control Panel</h5>
                    </div>
                    <div class="card-body">
                        <div class="btn-group" role="group">
                            <button type="button" class="btn btn-success" id="start-btn">
                                <i class="fas fa-play"></i> Start
                            </button>
                            <button type="button" class="btn btn-danger" id="stop-btn">
                                <i class="fas fa-stop"></i> Stop
                            </button>
                            <button type="button" class="btn btn-warning" id="pause-btn">
                                <i class="fas fa-pause"></i> Pause
                            </button>
                            <button type="button" class="btn btn-info" id="resume-btn">
                                <i class="fas fa-play"></i> Resume
                            </button>
                        </div>
                        <div class="mt-3">
                            <small class="text-muted" id="next-optimal-time">
                                Next optimal time: <span id="optimal-time">--</span>
                            </small>
                        </div>
                    </div>
                </div>
            </div>
        </div>

        <!-- Charts and Analytics -->
        <div class="row mb-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-line"></i> Daily Applications</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="dailyChart"></canvas>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-chart-pie"></i> Application Status</h5>
                    </div>
                    <div class="card-body">
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
            </div>
        </div>

        <!-- Recent Applications -->
        <div class="row">
            <div class="col-12">
                <div class="card">
                    <div class="card-header">
                        <h5><i class="fas fa-briefcase"></i> Recent Applications</h5>
                    </div>
                    <div class="card-body">
                        <div class="table-responsive">
                            <table class="table table-striped" id="applications-table">
                                <thead>
                                    <tr>
                                        <th>Date</th>
                                        <th>Job Title</th>
                                        <th>Company</th>
                                        <th>Status</th>
                                        <th>Easy Apply</th>
                                        <th>Actions</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    <!-- Applications will be loaded here -->
                                </tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.1.3/dist/js/bootstrap.bundle.min.js"></script>
    <script>
        // Global variables
        let dailyChart, statusChart;
        let updateInterval;

        // Initialize dashboard
        document.addEventListener('DOMContentLoaded', function() {
            initializeCharts();
            loadDashboardData();
            setupEventListeners();
            startAutoUpdate();
        });

        function initializeCharts() {
            // Daily applications chart
            const dailyCtx = document.getElementById('dailyChart').getContext('2d');
            dailyChart = new Chart(dailyCtx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Applications',
                        data: [],
                        borderColor: 'rgb(75, 192, 192)',
                        tension: 0.1
                    }]
                },
                options: {
                    responsive: true,
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });

            // Status chart
            const statusCtx = document.getElementById('statusChart').getContext('2d');
            statusChart = new Chart(statusCtx, {
                type: 'doughnut',
                data: {
                    labels: ['Applied', 'Interviewed', 'Rejected', 'Accepted'],
                    datasets: [{
                        data: [0, 0, 0, 0],
                        backgroundColor: [
                            '#007bff',
                            '#ffc107',
                            '#dc3545',
                            '#28a745'
                        ]
                    }]
                },
                options: {
                    responsive: true
                }
            });
        }

        function setupEventListeners() {
            document.getElementById('start-btn').addEventListener('click', startAutomation);
            document.getElementById('stop-btn').addEventListener('click', stopAutomation);
            document.getElementById('pause-btn').addEventListener('click', pauseAutomation);
            document.getElementById('resume-btn').addEventListener('click', resumeAutomation);
        }

        function startAutoUpdate() {
            updateInterval = setInterval(loadDashboardData, 30000); // Update every 30 seconds
        }

        async function loadDashboardData() {
            try {
                // Load status
                const statusResponse = await fetch('/api/status');
                const statusData = await statusResponse.json();
                updateStatus(statusData);

                // Load analytics
                const analyticsResponse = await fetch('/api/analytics');
                const analyticsData = await analyticsResponse.json();
                updateCharts(analyticsData);

                // Load applications
                const applicationsResponse = await fetch('/api/applications');
                const applicationsData = await applicationsResponse.json();
                updateApplicationsTable(applicationsData);

                // Update timestamp
                document.getElementById('update-time').textContent = new Date().toLocaleTimeString();
            } catch (error) {
                console.error('Error loading dashboard data:', error);
            }
        }

        function updateStatus(data) {
            const automation = data.automation;
            const scheduler = data.scheduler;

            // Update status
            const statusIcon = document.getElementById('status-icon');
            const statusText = document.getElementById('status-text');
            
            if (automation.is_running) {
                statusIcon.className = 'fas fa-play-circle fa-2x mb-2 status-running';
                statusText.textContent = 'Running';
            } else if (scheduler.is_paused) {
                statusIcon.className = 'fas fa-pause-circle fa-2x mb-2 status-paused';
                statusText.textContent = 'Paused';
            } else {
                statusIcon.className = 'fas fa-stop-circle fa-2x mb-2 status-stopped';
                statusText.textContent = 'Stopped';
            }

            // Update metrics
            document.getElementById('daily-applications').textContent = scheduler.applications_sent;
            document.getElementById('remaining-applications').textContent = scheduler.remaining_applications;
            document.getElementById('success-rate').textContent = '0%'; // Would calculate from analytics

            // Update next optimal time
            if (scheduler.next_optimal_time) {
                const nextTime = new Date(scheduler.next_optimal_time);
                document.getElementById('optimal-time').textContent = nextTime.toLocaleString();
            }
        }

        function updateCharts(data) {
            // Update daily chart
            if (data.daily_counts && data.daily_counts.length > 0) {
                const labels = data.daily_counts.map(item => item[0]);
                const counts = data.daily_counts.map(item => item[1]);
                
                dailyChart.data.labels = labels;
                dailyChart.data.datasets[0].data = counts;
                dailyChart.update();
            }

            // Update status chart
            if (data.status_breakdown) {
                const statusData = [
                    data.status_breakdown.applied || 0,
                    data.status_breakdown.interviewed || 0,
                    data.status_breakdown.rejected || 0,
                    data.status_breakdown.accepted || 0
                ];
                
                statusChart.data.datasets[0].data = statusData;
                statusChart.update();
            }
        }

        function updateApplicationsTable(applications) {
            const tbody = document.querySelector('#applications-table tbody');
            tbody.innerHTML = '';

            applications.forEach(app => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${new Date(app.application_date).toLocaleDateString()}</td>
                    <td>${app.job_title}</td>
                    <td>${app.company}</td>
                    <td><span class="badge bg-primary">${app.status}</span></td>
                    <td>${app.easy_apply ? '<i class="fas fa-check text-success"></i>' : '<i class="fas fa-times text-danger"></i>'}</td>
                    <td>
                        <button class="btn btn-sm btn-outline-primary" onclick="viewApplication(${app.id})">
                            <i class="fas fa-eye"></i>
                        </button>
                    </td>
                `;
                tbody.appendChild(row);
            });
        }

        async function startAutomation() {
            try {
                const response = await fetch('/api/control/start', { method: 'POST' });
                const result = await response.json();
                if (result.success) {
                    showAlert('Automation started successfully', 'success');
                } else {
                    showAlert('Failed to start automation: ' + result.message, 'danger');
                }
            } catch (error) {
                showAlert('Error starting automation: ' + error.message, 'danger');
            }
        }

        async function stopAutomation() {
            try {
                const response = await fetch('/api/control/stop', { method: 'POST' });
                const result = await response.json();
                if (result.success) {
                    showAlert('Automation stopped successfully', 'success');
                } else {
                    showAlert('Failed to stop automation: ' + result.message, 'danger');
                }
            } catch (error) {
                showAlert('Error stopping automation: ' + error.message, 'danger');
            }
        }

        async function pauseAutomation() {
            try {
                const response = await fetch('/api/control/pause', { 
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ duration: 60 })
                });
                const result = await response.json();
                if (result.success) {
                    showAlert('Automation paused for 60 minutes', 'warning');
                } else {
                    showAlert('Failed to pause automation: ' + result.message, 'danger');
                }
            } catch (error) {
                showAlert('Error pausing automation: ' + error.message, 'danger');
            }
        }

        async function resumeAutomation() {
            try {
                const response = await fetch('/api/control/resume', { method: 'POST' });
                const result = await response.json();
                if (result.success) {
                    showAlert('Automation resumed successfully', 'success');
                } else {
                    showAlert('Failed to resume automation: ' + result.message, 'danger');
                }
            } catch (error) {
                showAlert('Error resuming automation: ' + error.message, 'danger');
            }
        }

        function showAlert(message, type) {
            const alertDiv = document.createElement('div');
            alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
            alertDiv.innerHTML = `
                ${message}
                <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            `;
            
            const container = document.querySelector('.container-fluid');
            container.insertBefore(alertDiv, container.firstChild);
            
            // Auto-dismiss after 5 seconds
            setTimeout(() => {
                if (alertDiv.parentNode) {
                    alertDiv.remove();
                }
            }, 5000);
        }

        function viewApplication(id) {
            // This would open a modal or navigate to application details
            console.log('View application:', id);
        }
    </script>
</body>
</html>
    """
    
    with open(os.path.join(templates_dir, "dashboard.html"), 'w', encoding='utf-8') as f:
        f.write(dashboard_html)


if __name__ == "__main__":
    # Create templates
    create_dashboard_templates()
    
    # Start dashboard
    dashboard = WebDashboard(debug=True)
    dashboard.run()
