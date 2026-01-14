// General JavaScript for interactive features

document.addEventListener('DOMContentLoaded', function() {
    // Form validation
    const forms = document.querySelectorAll('.data-form');
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                return false;
            }
        });
    });

    // Confirmation dialogs
    const deleteButtons = document.querySelectorAll('.btn-danger');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (this.closest('form')) {
                const confirmed = confirm('Are you sure you want to delete this item?');
                if (!confirmed) {
                    e.preventDefault();
                    return false;
                }
            }
        });
    });
});

function validateForm(form) {
    let isValid = true;
    const inputs = form.querySelectorAll('input[required], textarea[required]');

    inputs.forEach(input => {
        if (!input.value.trim()) {
            isValid = false;
            input.style.borderColor = 'red';
            showError(input, 'This field is required');
        } else {
            input.style.borderColor = '';
            hideError(input);
        }
    });

    // Validate rank (1-10)
    const rankInputs = form.querySelectorAll('input[name="rank"], input[name="min_rank"]');
    rankInputs.forEach(input => {
        const value = parseInt(input.value);
        if (value < 1 || value > 10) {
            isValid = false;
            showError(input, 'Rank must be between 1 and 10');
        }
    });

    // Validate priority (1-10)
    const priorityInput = form.querySelector('input[name="priority"]');
    if (priorityInput) {
        const value = parseInt(priorityInput.value);
        if (value < 1 || value > 10) {
            isValid = false;
            showError(priorityInput, 'Priority must be between 1 and 10');
        }
    }

    // Validate hours
    const hoursInput = form.querySelector('input[name="max_hours"], input[name="duration"]');
    if (hoursInput) {
        const value = parseFloat(hoursInput.value);
        if (value <= 0) {
            isValid = false;
            showError(hoursInput, 'Hours must be greater than 0');
        }
    }

    return isValid;
}

function showError(input, message) {
    hideError(input);
    const error = document.createElement('div');
    error.className = 'error-message';
    error.style.color = 'red';
    error.style.fontSize = '0.85rem';
    error.style.marginTop = '0.25rem';
    error.textContent = message;
    input.parentNode.appendChild(error);
}

function hideError(input) {
    const existingError = input.parentNode.querySelector('.error-message');
    if (existingError) {
        existingError.remove();
    }
}

// Update range slider values
function updateRangeValue(sliderId, valueId) {
    const slider = document.getElementById(sliderId);
    const valueDisplay = document.getElementById(valueId);

    if (slider && valueDisplay) {
        slider.addEventListener('input', function() {
            valueDisplay.textContent = this.value;
        });
    }
}

// Initialize tooltips
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = this.getAttribute('data-tooltip');
            tooltip.style.position = 'absolute';
            tooltip.style.backgroundColor = '#333';
            tooltip.style.color = 'white';
            tooltip.style.padding = '0.5rem';
            tooltip.style.borderRadius = '4px';
            tooltip.style.fontSize = '0.85rem';
            tooltip.style.zIndex = '1000';
            document.body.appendChild(tooltip);

            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + 'px';
            tooltip.style.top = (rect.bottom + 5) + 'px';
        });

        element.addEventListener('mouseleave', function() {
            const tooltips = document.querySelectorAll('.tooltip');
            tooltips.forEach(t => t.remove());
        });
    });
}

// Auto-dismiss alerts
function autoDismissAlerts() {
    const alerts = document.querySelectorAll('.alert-dismissible');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => alert.remove(), 300);
        }, 5000);
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initTooltips();
    autoDismissAlerts();
});
