// Main JavaScript for Eco Impact Tracker

// Initialize tooltips
const initTooltips = () => {
    const tooltips = document.querySelectorAll('[data-tooltip]');
    tooltips.forEach(element => {
        const tooltip = element.getAttribute('data-tooltip');
        element.title = tooltip;
    });
};

// Progress bar animations
const initProgressBars = () => {
    const progressBars = document.querySelectorAll('.progress-bar-fill');
    progressBars.forEach(bar => {
        const target = bar.getAttribute('data-target');
        bar.style.width = target + '%';
    });
};

// Activity form validation
const initActivityForm = () => {
    const form = document.getElementById('activity-form');
    if (!form) return;

    form.addEventListener('submit', (e) => {
        const category = form.querySelector('[name="category"]').value;
        const description = form.querySelector('[name="description"]').value;
        const activityData = form.querySelector('[name="activity_data"]').value;

        if (!category || !description || !activityData) {
            e.preventDefault();
            alert('Please fill in all fields');
        }
    });
};

// Challenge countdown timer
const initCountdownTimer = () => {
    const timers = document.querySelectorAll('.countdown-timer');
    
    timers.forEach(timer => {
        const endDate = new Date(timer.getAttribute('data-end-date')).getTime();
        
        const updateTimer = () => {
            const now = new Date().getTime();
            const distance = endDate - now;
            
            if (distance < 0) {
                timer.innerHTML = 'Challenge ended';
                return;
            }
            
            const days = Math.floor(distance / (1000 * 60 * 60 * 24));
            const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
            const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
            
            timer.innerHTML = `${days}d ${hours}h ${minutes}m`;
        };
        
        updateTimer();
        setInterval(updateTimer, 60000); // Update every minute
    });
};

// Chart animations
const initChartAnimations = () => {
    const charts = document.querySelectorAll('.chart-container');
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-float');
            }
        });
    }, { threshold: 0.5 });
    
    charts.forEach(chart => observer.observe(chart));
};

// Mobile menu toggle
const initMobileMenu = () => {
    const menuButton = document.getElementById('mobile-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');
    
    if (!menuButton || !mobileMenu) return;
    
    menuButton.addEventListener('click', () => {
        mobileMenu.classList.toggle('hidden');
    });
};

// Like/vote functionality
const initLikeButtons = () => {
    const likeButtons = document.querySelectorAll('.like-button');
    
    likeButtons.forEach(button => {
        button.addEventListener('click', async () => {
            const postId = button.getAttribute('data-post-id');
            const response = await fetch(`/api/like/${postId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                }
            });
            
            if (response.ok) {
                const data = await response.json();
                button.querySelector('.like-count').textContent = data.likes;
                button.classList.toggle('liked');
            }
        });
    });
};

// Smart device integration
const initSmartDevices = () => {
    const deviceWidgets = document.querySelectorAll('.smart-device-widget');
    
    deviceWidgets.forEach(widget => {
        const updateWidget = async () => {
            const deviceId = widget.getAttribute('data-device-id');
            try {
                const response = await fetch(`/api/device/${deviceId}/status`);
                const data = await response.json();
                
                widget.querySelector('.device-status').textContent = data.status;
                widget.querySelector('.energy-usage').textContent = 
                    `${data.energy_usage} kWh`;
            } catch (error) {
                console.error('Failed to update device status:', error);
            }
        };
        
        updateWidget();
        setInterval(updateWidget, 300000); // Update every 5 minutes
    });
};

// Initialize all components
document.addEventListener('DOMContentLoaded', () => {
    initTooltips();
    initProgressBars();
    initActivityForm();
    initCountdownTimer();
    initChartAnimations();
    initMobileMenu();
    initLikeButtons();
    initSmartDevices();
});

// Handle form submissions with AJAX
const handleAjaxForms = () => {
    const ajaxForms = document.querySelectorAll('form[data-ajax]');
    
    ajaxForms.forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const formData = new FormData(form);
            const submitButton = form.querySelector('[type="submit"]');
            
            try {
                submitButton.disabled = true;
                submitButton.innerHTML = 'Submitting...';
                
                const response = await fetch(form.action, {
                    method: form.method,
                    body: formData
                });
                
                const data = await response.json();
                
                if (data.success) {
                    showNotification(data.message, 'success');
                    if (data.redirect) {
                        window.location.href = data.redirect;
                    }
                } else {
                    showNotification(data.message, 'error');
                }
            } catch (error) {
                showNotification('An error occurred. Please try again.', 'error');
            } finally {
                submitButton.disabled = false;
                submitButton.innerHTML = 'Submit';
            }
        });
    });
};

// Notification system
const showNotification = (message, type = 'info') => {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <p>${message}</p>
            <button class="notification-close">&times;</button>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('notification-show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('notification-show');
        setTimeout(() => notification.remove(), 300);
    }, 5000);
    
    notification.querySelector('.notification-close').addEventListener('click', () => {
        notification.classList.remove('notification-show');
        setTimeout(() => notification.remove(), 300);
    });
};

// Initialize AJAX form handling
document.addEventListener('DOMContentLoaded', handleAjaxForms);
