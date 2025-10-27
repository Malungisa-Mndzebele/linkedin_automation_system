/**
 * Configuration JavaScript
 * Handles the configuration page functionality
 */

// Global variables
let currentConfig = {};

// Initialize configuration page
document.addEventListener('DOMContentLoaded', function() {
    loadCurrentConfig();
    setupEventListeners();
    updateConfigPreview();
});

// Setup event listeners
function setupEventListeners() {
    // Form submission
    document.getElementById('config-form').addEventListener('submit', function(e) {
        e.preventDefault();
        saveConfiguration();
    });
    
    // Load config button
    document.getElementById('load-config').addEventListener('click', function() {
        loadCurrentConfig();
    });
    
    // Form field changes
    const formFields = document.querySelectorAll('#config-form input, #config-form select');
    formFields.forEach(field => {
        field.addEventListener('change', updateConfigPreview);
        field.addEventListener('input', updateConfigPreview);
    });
}

// Load current configuration
async function loadCurrentConfig() {
    try {
        const response = await fetch('/api/config');
        const config = await response.json();
        
        currentConfig = config;
        populateForm(config);
        updateConfigPreview();
        
        showAlert('Configuration loaded successfully', 'success');
    } catch (error) {
        console.error('Error loading configuration:', error);
        showAlert('Error loading configuration', 'danger');
    }
}

// Populate form with configuration data
function populateForm(config) {
    // Basic fields
    document.getElementById('email').value = config.email || '';
    document.getElementById('password').value = config.password || '';
    document.getElementById('job_keywords').value = Array.isArray(config.job_keywords) 
        ? config.job_keywords.join(', ') 
        : config.job_keywords || '';
    document.getElementById('location').value = config.preferred_location || '';
    document.getElementById('max_applications').value = config.max_applications_per_day || 10;
    
    // Checkboxes
    document.getElementById('easy_apply_only').checked = config.easy_apply_only !== false;
    document.getElementById('headless').checked = config.headless === true;
    document.getElementById('remote_preference').checked = config.remote_preference === true;
    
    // Select fields
    document.getElementById('experience_level').value = config.experience_level || 'mid';
    document.getElementById('company_size').value = config.company_size || 'medium';
    
    // Additional fields
    document.getElementById('experience_years').value = config.experience_years || 3;
    document.getElementById('skills').value = Array.isArray(config.skills) 
        ? config.skills.join(', ') 
        : config.skills || '';
    document.getElementById('education').value = Array.isArray(config.education) 
        ? config.education.join(', ') 
        : config.education || '';
    document.getElementById('preferred_industries').value = Array.isArray(config.preferred_industries) 
        ? config.preferred_industries.join(', ') 
        : config.preferred_industries || '';
}

// Save configuration
async function saveConfiguration() {
    try {
        const formData = new FormData(document.getElementById('config-form'));
        const config = {};
        
        // Process form data
        for (let [key, value] of formData.entries()) {
            if (key === 'job_keywords' || key === 'skills' || key === 'education' || key === 'preferred_industries') {
                config[key] = value.split(',').map(item => item.trim()).filter(item => item);
            } else if (key === 'max_applications_per_day' || key === 'experience_years') {
                config[key] = parseInt(value);
            } else if (key === 'easy_apply_only' || key === 'headless' || key === 'remote_preference') {
                config[key] = true; // Only included if checked
            } else {
                config[key] = value;
            }
        }
        
        // Handle checkboxes that weren't submitted
        if (!formData.has('easy_apply_only')) config.easy_apply_only = false;
        if (!formData.has('headless')) config.headless = false;
        if (!formData.has('remote_preference')) config.remote_preference = false;
        
        // Validate required fields
        if (!config.email || !config.password || !config.job_keywords) {
            showAlert('Please fill in all required fields', 'warning');
            return;
        }
        
        // Save configuration
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(config)
        });
        
        const result = await response.json();
        
        if (result.success) {
            showAlert('Configuration saved successfully!', 'success');
            currentConfig = config;
            updateConfigPreview();
        } else {
            showAlert(result.error || 'Failed to save configuration', 'danger');
        }
    } catch (error) {
        console.error('Error saving configuration:', error);
        showAlert('Error saving configuration', 'danger');
    }
}

// Update configuration preview
function updateConfigPreview() {
    const formData = new FormData(document.getElementById('config-form'));
    const config = {};
    
    // Process form data
    for (let [key, value] of formData.entries()) {
        if (key === 'job_keywords' || key === 'skills' || key === 'education' || key === 'preferred_industries') {
            config[key] = value.split(',').map(item => item.trim()).filter(item => item);
        } else if (key === 'max_applications_per_day' || key === 'experience_years') {
            config[key] = parseInt(value);
        } else if (key === 'easy_apply_only' || key === 'headless' || key === 'remote_preference') {
            config[key] = true;
        } else {
            config[key] = value;
        }
    }
    
    // Handle checkboxes
    if (!formData.has('easy_apply_only')) config.easy_apply_only = false;
    if (!formData.has('headless')) config.headless = false;
    if (!formData.has('remote_preference')) config.remote_preference = false;
    
    // Update preview
    const previewElement = document.getElementById('config-preview');
    previewElement.textContent = JSON.stringify(config, null, 2);
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

// Form validation
function validateForm() {
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;
    const jobKeywords = document.getElementById('job_keywords').value;
    
    if (!email || !password || !jobKeywords) {
        showAlert('Please fill in all required fields', 'warning');
        return false;
    }
    
    if (!email.includes('@')) {
        showAlert('Please enter a valid email address', 'warning');
        return false;
    }
    
    return true;
}

// Auto-save configuration every 30 seconds
setInterval(() => {
    if (document.getElementById('config-form').checkValidity()) {
        updateConfigPreview();
    }
}, 30000);
