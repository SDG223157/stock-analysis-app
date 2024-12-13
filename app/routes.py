from flask import Blueprint, render_template, request, make_response
from datetime import datetime
import logging
import traceback
from app.utils.analysis import create_combined_analysis

bp = Blueprint('main', __name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@bp.route('/')
def index():
    # Pass today's date as max date for the date input
    today = datetime.now().strftime('%Y-%m-%d')
    return render_template('index.html', now=datetime.now(), max_date=today)

@bp.route('/analyze', methods=['POST'])
def analyze():
    try:
        # Extract and validate form data
        ticker = request.form.get('ticker')
        if not ticker:
            raise ValueError("Ticker symbol is required")
        
        # Handle end_date (optional)
        end_date = request.form.get('end_date')
        if end_date:
            try:
                # Validate date format
                datetime.strptime(end_date, '%Y-%m-%d')
            except ValueError:
                raise ValueError("Invalid date format. Please use YYYY-MM-DD format")
        else:
            end_date = None  # If no date provided, use None
            
        try:
            lookback_days = int(request.form.get('lookback_days', 365))
            if lookback_days < 30 or lookback_days > 1825:
                raise ValueError
        except ValueError:
            raise ValueError("Lookback days must be between 30 and 1825")
            
        try:
            crossover_days = int(request.form.get('crossover_days', 180))
            if crossover_days < 30 or crossover_days > 365:
                raise ValueError
        except ValueError:
            raise ValueError("Crossover days must be between 30 and 365")
        
        logger.info(f"Analyzing ticker: {ticker}, end_date: {end_date}, "
                   f"lookback_days: {lookback_days}, crossover_days: {crossover_days}")
        
        # Perform analysis
        _, fig, _, _ = create_combined_analysis(
            ticker,
            end_date=end_date,
            lookback_days=lookback_days,
            crossover_days=crossover_days
        )
        
        # Generate HTML
        html_content = fig.to_html(
            full_html=True,
            include_plotlyjs=True,
            config={'responsive': True}
        )
        
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'
        return response
        
    except ValueError as e:
        logger.warning(f"Validation error: {str(e)}")
        error_html = f"""
        <html>
            <head>
                <title>Error</title>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 2rem; }}
                    .error {{ color: #dc3545; padding: 1rem; background-color: #f8d7da; 
                             border: 1px solid #f5c6cb; border-radius: 3px; }}
                    .back-link {{ margin-top: 1rem; display: block; }}
                </style>
            </head>
            <body>
                <div class="error">
                    <h2>Input Error</h2>
                    <p>{str(e)}</p>
                </div>
                <a href="javascript:window.close();" class="back-link">Close Window</a>
            </body>
        </html>
        """
        return error_html, 400
        
    except Exception as e:
        logger.error(f"Analysis error: {str(e)}\n{traceback.format_exc()}")
        error_html = f"""
        <html>
            <head>
                <title>Error</title>
                <style>
                    body {{ font-family: Arial, sans-serif; padding: 2rem; }}
                    .error {{ color: #dc3545; padding: 1rem; background-color: #f8d7da; 
                             border: 1px solid #f5c6cb; border-radius: 3px; }}
                    .back-link {{ margin-top: 1rem; display: block; }}
                </style>
            </head>
            <body>
                <div class="error">
                    <h2>Analysis Error</h2>
                    <p>Failed to analyze ticker. Error: {str(e)}</p>
                </div>
                <a href="javascript:window.close();" class="back-link">Close Window</a>
            </body>
        </html>
        """
        return error_html, 500
