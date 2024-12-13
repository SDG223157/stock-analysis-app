from flask import Blueprint, render_template, request, make_response
from app.utils.analysis import create_combined_analysis
import traceback

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/analyze', methods=['POST'])
def analyze():
    try:
        ticker = request.form['ticker']
        end_date = request.form.get('end_date', None)
        lookback_days = int(request.form.get('lookback_days', 365))
        crossover_days = int(request.form.get('crossover_days', 180))
        
        _, fig, _, _ = create_combined_analysis(
            ticker,
            end_date=end_date,
            lookback_days=lookback_days,
            crossover_days=crossover_days
        )
        
        html_content = fig.to_html(
            full_html=True,
            include_plotlyjs=True,
            config={'responsive': True}
        )
        
        response = make_response(html_content)
        response.headers['Content-Type'] = 'text/html'
        return response
        
    except Exception as e:
        return f"Error: {str(e)}", 500
