/**
 * Monitor JavaScript
 * Handles the live monitoring functionality
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
    },
    sessionStartTime: null,
    currentJob: null
};

// Initialize monitor
document.addEventListener('DOMContentLoaded', function() {
    initializeSocket();
    loadAutomationStatus();
    startSessionTimer();
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

// Load automation status
async function loadAutomationStatus() {
    try {
        const response = await fetch('/api/automation/status');
        const data = await response.json();
        
        automationStatus = data;
        updateMonitorDisplay();
    } catch (error) {
        console.error('Error loading automation status:', error);
    }
}

// Handle automation updates
function handleAutomationUpdate(data) {
    console.log('Automation update:', data);
    
    switch (data.event) {
        case 'jobs_found':
            automationStatus.stats.jobs_found = data.data;
            addActivityFeed('info', `Found ${data.data} jobs`, data.timestamp);
            break;
        case 'application_success':
            automationStatus.stats.applications_sent = data.data.total;
            addActivityFeed('success', `Applied to ${data.data.title} at ${data.data.company}`, data.timestamp);
            addRecentApplication(data.data, 'success');
            break;
        case 'application_failed':
            addActivityFeed('danger', `Failed to apply to ${data.data.title} at ${data.data.company}`, data.timestamp);
            addRecentApplication(data.data, 'failed');
            break;
        case 'current_job':
            automationStatus.currentJob = data.data;
            updateCurrentJob(data.data);
            addActivityFeed('info', `Processing: ${data.data.title} at ${data.data.company}`, data.timestamp);
            break;
        case 'automation_complete':
            automationStatus.isRunning = false;
            automationStatus.stats = data.data;
            addActivityFeed('success', 'Automation completed successfully!', data.timestamp);
            updateCurrentJob(null);
            break;
        case 'automation_stopped':
            automationStatus.isRunning = false;
            addActivityFeed('warning', 'Automation stopped by user', data.timestamp);
            updateCurrentJob(null);
            break;
        case 'daily_limit_reached':
            addActivityFeed('warning', 'Daily application limit reached', data.timestamp);
            break;
    }
    
    updateMonitorDisplay();
}

// Handle automation errors
function handleAutomationError(data) {
    console.error('Automation error:', data);
    automationStatus.stats.errors_count++;
    addActivityFeed('danger', `Error: ${data.message}`, data.timestamp);
    updateMonitorDisplay();
}

// Update monitor display
function updateMonitorDisplay() {
    // Update automation status
    const statusElement = document.getElementById('automation-status');
    if (automationStatus.isRunning) {
        statusElement.textContent = 'Running';
        statusElement.className = 'text-success';
    } else {
        statusElement.textContent = 'Stopped';
        statusElement.className = 'text-danger';
    }
    
    // Update statistics
    document.getElementById('total-jobs').textContent = automationStatus.stats.jobs_found || 0;
    document.getElementById('success-rate').textContent = (automationStatus.stats.success_rate || 0) + '%';
    document.getElementById('errors-count').textContent = automationStatus.stats.errors_count || 0;
    document.getElementById('applications-sent').textContent = automationStatus.stats.applications_sent || 0;
    
    // Calculate remaining applications
    const maxApps = automationStatus.config?.max_applications_per_day || 10;
    const remaining = maxApps - (automationStatus.stats.applications_sent || 0);
    document.getElementById('remaining-apps').textContent = Math.max(0, remaining);
    
    // Update jobs processed
    document.getElementById('jobs-processed').textContent = automationStatus.stats.jobs_found || 0;
}

// Update current job display
function updateCurrentJob(jobData) {
    const currentJobElement = document.getElementById('current-job');
    const progressBar = document.getElementById('progress-bar');
    
    if (jobData) {
        currentJobElement.innerHTML = `
            <div class="text-center">
                <i class="fas fa-briefcase fa-3x text-primary"></i>
                <h5 class="mt-2">${jobData.title}</h5>
                <p class="text-muted">at ${jobData.company}</p>
                <small class="text-info">Job ${jobData.number}</small>
            </div>
        `;
        progressBar.style.display = 'block';
    } else {
        currentJobElement.innerHTML = `
            <i class="fas fa-pause-circle fa-3x text-muted"></i>
            <p class="mt-2 text-muted">No active automation</p>
        `;
        progressBar.style.display = 'none';
    }
}

// Add activity feed entry
function addActivityFeed(type, message, timestamp) {
    const feedElement = document.getElementById('activity-feed');
    
    // Remove "waiting" message if it exists
    const waitingMsg = feedElement.querySelector('.text-center.text-muted');
    if (waitingMsg) {
        waitingMsg.remove();
    }
    
    const time = new Date(timestamp).toLocaleTimeString();
    const typeClass = type === 'success' ? 'success' : type === 'danger' ? 'danger' : type === 'warning' ? 'warning' : 'info';
    const typeIcon = type === 'success' ? 'check-circle' : type === 'danger' ? 'times-circle' : type === 'warning' ? 'exclamation-triangle' : 'info-circle';
    
    const feedEntry = document.createElement('div');
    feedEntry.className = 'd-flex align-items-center p-2 border-bottom';
    feedEntry.innerHTML = `
        <div class="flex-shrink-0 me-3">
            <i class="fas fa-${typeIcon} text-${typeClass}"></i>
        </div>
        <div class="flex-grow-1">
            <div class="fw-bold">${message}</div>
            <small class="text-muted">${time}</small>
        </div>
    `;
    
    feedElement.insertBefore(feedEntry, feedElement.firstChild);
    
    // Keep only last 20 entries
    const entries = feedElement.querySelectorAll('.d-flex');
    if (entries.length > 20) {
        entries[entries.length - 1].remove();
    }
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
    
    // Keep only last 10 applications
    const applications = container.querySelectorAll('.d-flex');
    if (applications.length > 10) {
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

// Start session timer
function startSessionTimer() {
    setInterval(() => {
        if (automationStatus.isRunning && automationStatus.sessionStartTime) {
            const startTime = new Date(automationStatus.sessionStartTime);
            const now = new Date();
            const duration = now - startTime;
            
            const hours = Math.floor(duration / 3600000);
            const minutes = Math.floor((duration % 3600000) / 60000);
            const seconds = Math.floor((duration % 60000) / 1000);
            
            const timeString = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
            document.getElementById('session-duration').textContent = timeString;
        } else {
            document.getElementById('session-duration').textContent = '00:00:00';
        }
    }, 1000);
}

// Clear activity feed
document.getElementById('clear-feed').addEventListener('click', function() {
    const feedElement = document.getElementById('activity-feed');
    feedElement.innerHTML = `
        <div class="text-center text-muted">
            <i class="fas fa-info-circle"></i>
            <p>Activity feed cleared</p>
        </div>
    `;
});

// Refresh status every 10 seconds
setInterval(() => {
    loadAutomationStatus();
}, 10000);
