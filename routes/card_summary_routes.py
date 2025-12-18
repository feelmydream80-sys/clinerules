# routes/card_summary_routes.py
from flask import Blueprint, render_template, jsonify, session
from service.card_summary_service import CardSummaryService
from msys.database import get_db_connection
from flask_login import login_required
from routes.admin_routes import log_menu_access
from routes.auth_routes import card_summary_required

card_summary_bp = Blueprint('card_summary', __name__)

@card_summary_bp.route('/card_summary')
@login_required
@card_summary_required
@log_menu_access
def card_summary_page():
    """
    Renders the card summary page.
    """
    return render_template('card_summary.html')

@card_summary_bp.route('/api/card_summary')
@login_required
@card_summary_required
def get_card_summary_data():
    """
    Provides card summary data as JSON.
    """
    db_connection = get_db_connection()
    service = CardSummaryService(db_connection)
    user = session.get('user')
    summary_data = service.get_card_summary(user)
    return jsonify(summary_data)
