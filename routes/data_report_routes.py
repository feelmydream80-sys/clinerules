from flask import Blueprint, render_template, session, current_app, request, jsonify
from functools import wraps
from .auth_routes import login_required, check_password_change_required
from routes.ui.dashboard_routes import log_menu_access
from service.dashboard_service import DashboardService
from mapper.mst_mapper import MstMapper
from mapper.user_mapper import UserMapper
from msys.database import get_db_connection
from datetime import datetime, timedelta
import croniter
import pytz

data_report_bp = Blueprint('data_report', __name__)
