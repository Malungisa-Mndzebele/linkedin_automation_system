/**
 * Dashboard JavaScript
 * Handles the main dashboard functionality
 */

// Global variables
let socket;
let automationStatus = {
    isRunning: false,
    stats: {
        jobs_found: 0,
        applications_sent: 0,
        success_rate: 0,
        errors_count: 0
    }
};

// Initialize dashboard
document.addEventListener('DOMContentLoaded', function() {
    initializeSocket();
    loadAutomationStatus();
    setupEventListeners();
    updateDashboard();
});

// Initialize Socket.IO connection
function initializeSocket() {
    socket = io();
    
    socket.on('connect', function() {
        console.log('Connected to server');
        updateConnectionStatus(true);
    });
    
    socket.on('disconnect', function() {
        console.log('Disconnected from server');
        updateConnectionStatus(false);
    });
    
    socket.on('automation_update', function(data) {
        handleAutomationUpdate(data);
    });
    
    socket.on('automation_error', function(data) {
        handleAutomationError(data);
    });
}

// Setup event listeners
function setupEventListeners() {
    // Start automation button
    document.getElementById('start-automation').addEventListener('click', function() {
        startAutomation();
    });
    
    // Stop automation button
    document.getElementById('stop-automation').addEventListener('click', function() {
        stopAutomation();
    });
}

// Load automation status
async function loadAutomationStatus() {
    try {
        const response = await fetch('/api/automation/status');
        const data = await response.json();
        
        automationStatus = data;
        updateDashboard();
    } catch (error) {
        console.error('Error loading automation status:', error);
    }
}

// Start automation
async function startAutomation() {
    try {
        // Load current configuration
        const configResponse = await fetch('/api/config');
        const config = await configResponse.json();
        
        if (!config.email || !config.password || !config.job_keywords) {
            showAlert('Please configure your settings first', 'warning');
            return;
        }
        
        // Start automation
        const response = await fetch('/api/automation/start', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Automation started successfully!', 'success');
            automationStatus.isRunning = true;
            updateDashboard();
        } else {
            showAlert(result.error || 'Failed to start automation', 'danger');
        }
    } catch (error) {
        console.error('Error starting automation:', error);
        showAlert('Error starting automation', 'danger');
    }
}

// Stop automation
async function stopAutomation() {
    try {
        const response = await fetch('/api/automation/stop', {
            method: 'POST'
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Automation stopped successfully!', 'info');
            automationStatus.isRunning = false;
            updateDashboard();
        } else {
            showAlert(result.error || 'Failed to stop automation', 'danger');
        }
    } catch (error) {
        console.error('Error stopping automation:', error);
        showAlert('Error stopping automation', 'danger');
    }
}

// Handle automation updates
function handleAutomationUpdate(data) {
    console.log('Automation update:', data);
    
    switch (data.event) {
        case 'jobs_found':
            automationStatus.stats.jobs_found = data.data;
            break;
        case 'application_success':
            automationStatus.stats.applications_sent = data.data.total;
            addRecentApplication(data.data, 'success');
            break;
        case 'application_failed':
            addRecentApplication(data.data, 'failed');
            break;
        case 'current_job':
            updateCurrentActivity(data.data);
            break;
        case 'automation_complete':
            automationStatus.isRunning = false;
            automationStatus.stats = data.data;
            showAlert('Automation completed successfully!', 'success');
            break;
        case 'automation_stopped':
            automationStatus.isRunning = false;
            showAlert('Automation stopped', 'info');
            break;
        case 'daily_limit_reached':
            showAlert('Daily application limit reached', 'warning');
            break;
    }
    
    updateDashboard();
}

// Handle automation errors
function handleAutomationError(data) {
    console.error('Automation error:', data);
    automationStatus.stats.errors_count++;
    showAlert(data.message, 'danger');
    updateDashboard();
}

// Update dashboard display
function updateDashboard() {
    // Update status banner
    const statusBanner = document.getElementById('status-banner');
    const statusText = document.getElementById('status-text');
    
    if (automationStatus.isRunning) {
        statusBanner.className = 'alert alert-success';
        statusText.textContent = 'Automation is running...';
    } else {
        statusBanner.className = 'alert alert-info';
        statusText.textContent = 'Automation is ready to start';
    }
    
    // Update buttons
    const startBtn = document.getElementById('start-automation');
    const stopBtn = document.getElementById('stop-automation');
    
    if (automationStatus.isRunning) {
        startBtn.disabled = true;
        stopBtn.disabled = false;
    } else {
        startBtn.disabled = false;
        stopBtn.disabled = true;
    }
    
    // Update statistics
    document.getElementById('jobs-found').textContent = automationStatus.stats.jobs_found || 0;
    document.getElementById('applications-sent').textContent = automationStatus.stats.applications_sent || 0;
    document.getElementById('success-rate').textContent = (automationStatus.stats.success_rate || 0) + '%';
    document.getElementById('errors-count').textContent = automationStatus.stats.errors_count || 0;
    
    // Update current activity
    if (!automationStatus.isRunning) {
        document.getElementById('current-activity').innerHTML = `
            <i class="fas fa-pause-circle fa-3x text-muted"></i>
            <p class="mt-2 text-muted">No active automation</p>
        `;
    }
}

// Update current activity display
function updateCurrentActivity(jobData) {
    document.getElementById('current-activity').innerHTML = `
        <div class="text-center">
            <i class="fas fa-briefcase fa-3x text-primary"></i>
            <h5 class="mt-2">${jobData.title}</h5>
            <p class="text-muted">at ${jobData.company}</p>
            <small class="text-info">Job ${jobData.number}</small>
        </div>
    `;
}

// Add recent application
function addRecentApplication(jobData, status) {
    const container = document.getElementById('recent-applications');
    
    // Remove "no applications" message if it exists
    const noAppsMsg = container.querySelector('.text-muted.text-center');
    if (noAppsMsg) {
        noAppsMsg.remove();
    }
    
    const statusClass = status === 'success' ? 'success' : 'danger';
    const statusIcon = status === 'success' ? 'check-circle' : 'times-circle';
    
    const applicationDiv = document.createElement('div');
    applicationDiv.className = 'd-flex justify-content-between align-items-center p-2 border-bottom';
    applicationDiv.innerHTML = `
        <div>
            <strong>${jobData.title}</strong>
            <br>
            <small class="text-muted">${jobData.company}</small>
        </div>
        <div>
            <span class="badge bg-${statusClass}">
                <i class="fas fa-${statusIcon}"></i> ${status.toUpperCase()}
            </span>
        </div>
    `;
    
    container.insertBefore(applicationDiv, container.firstChild);
    
    // Keep only last 5 applications
    const applications = container.querySelectorAll('.d-flex');
    if (applications.length > 5) {
        applications[applications.length - 1].remove();
    }
}

// Update connection status
function updateConnectionStatus(connected) {
    const statusElement = document.getElementById('connection-status');
    if (connected) {
        statusElement.className = 'badge bg-success fs-6';
        statusElement.innerHTML = '<i class="fas fa-circle"></i> Connected';
    } else {
        statusElement.className = 'badge bg-danger fs-6';
        statusElement.innerHTML = '<i class="fas fa-circle"></i> Disconnected';
    }
}

// Show alert message
function showAlert(message, type) {
    // Remove existing alerts
    const existingAlerts = document.querySelectorAll('.alert-dismissible');
    existingAlerts.forEach(alert => alert.remove());
    
    // Create new alert
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type} alert-dismissible fade show`;
    alertDiv.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    // Insert at top of container
    const container = document.querySelector('.container');
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-dismiss after 5 seconds
    setTimeout(() => {
        if (alertDiv.parentNode) {
            alertDiv.remove();
        }
    }, 5000);
}

// Refresh dashboard every 30 seconds
setInterval(() => {
    if (!automationStatus.isRunning) {
        loadAutomationStatus();
    }
}, 30000);
