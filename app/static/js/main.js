document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('analysis-form');
    const loadingDiv = document.createElement('div');
    loadingDiv.className = 'loading';
    loadingDiv.innerHTML = 'Analyzing data, please wait...';
    form.appendChild(loadingDiv);
    
    form.addEventListener('submit', function(e) {
        // Clear any existing error messages
        const existingErrors = document.querySelectorAll('.error-message');
        existingErrors.forEach(error => error.remove());
        
        // Validate ticker
        const ticker = document.getElementById('ticker').value.trim();
        if (!ticker) {
            e.preventDefault();
            showError('ticker', 'Please enter a stock ticker symbol');
            return;
        }
        
        // Validate date if provided
        const endDate = document.getElementById('end_date').value;
        if (endDate) {
            const selectedDate = new Date(endDate);
            const today = new Date();
            if (selectedDate > today) {
                e.preventDefault();
                showError('end_date', 'End date cannot be in the future');
                return;
            }
        }
        
        // Validate lookback days
        const lookbackDays = parseInt(document.getElementById('lookback_days').value);
        if (isNaN(lookbackDays) || lookbackDays < 30 || lookbackDays > 1825) {
            e.preventDefault();
            showError('lookback_days', 'Lookback days must be between 30 and 1825');
            return;
        }
        
        // Validate crossover days
        const crossoverDays = parseInt(document.getElementById('crossover_days').value);
        if (isNaN(crossoverDays) || crossoverDays < 30 || crossoverDays > 365) {
            e.preventDefault();
            showError('crossover_days', 'Crossover days must be between 30 and 365');
            return;
        }
        
        // Show loading message
        loadingDiv.style.display = 'block';
        
        // Hide loading after submission to new window
        setTimeout(() => {
            loadingDiv.style.display = 'none';
        }, 1000);
    });
    
    function showError(fieldId, message) {
        const field = document.getElementById(fieldId);
        const errorDiv = document.createElement('div');
        errorDiv.className = 'error-message';
        errorDiv.textContent = message;
        field.parentNode.appendChild(errorDiv);
        field.focus();
    }
});
