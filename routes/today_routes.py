from flask import Blueprint
from datetime import datetime
import pytz

today_bp = Blueprint('today', __name__)

@today_bp.route('/api/today_date')
def get_today_date():
    kst = pytz.timezone('Asia/Seoul')
    today = datetime.now(kst).strftime('%Y-%m-%d')
    return {'today_date': today}
