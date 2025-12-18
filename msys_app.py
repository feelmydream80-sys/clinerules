#
# 주요 역할: Flask 애플리케이션의 메인 파일로, 라우팅, 서비스 계층 호출, 데이터베이스 연결 관리 등을 담당합니다.

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, g, flash
from flask_cors import CORS
from flasgger import Swagger
from flask_login import LoginManager
import logging
import logging.handlers
import sys
from datetime import datetime, timedelta, date
import decimal  # Decimal도 처리하려면
import json
import os
from dotenv import load_dotenv
load_dotenv()

from routes import init_app as init_routes
from msys.database import close_db_connection, init_db_pool
from routes.admin_routes import admin_bp

# --- 인증 기능 활성화 플래그 ---
AUTH_ENABLED = True
# --------------------------

# True로 설정하면 개발 모드(상세 로그), False로 설정하면 운영 모드(간결한 로그)로 동작합니다.
# .env 파일에서 FLASK_DEBUG 값을 읽어 디버그 모드를 설정합니다.
# '1' 또는 'true'로 설정하면 개발 모드(디버그, 자동 리로드 활성화)로 동작합니다.
FLASK_DEBUG = os.getenv('FLASK_DEBUG', '0').lower() in ['true', '1']

def create_app():
    app = Flask(__name__, static_folder='static', static_url_path='/static')
    class CustomJSONEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, (datetime, date)):
                return obj.isoformat()  # "2025-12-16T10:30:00" 또는 "2025-12-16" 형식
            if isinstance(obj, decimal.Decimal):
                return float(obj)  # 또는 str(obj)로 정확도 100% 보장
            # 필요시 다른 타입 추가 (예: bytes, set 등)
            try:
                return super().default(obj)
            except TypeError:
                return str(obj)  # 최후의 안전장치
    
    app.json_encoder = CustomJSONEncoder  # ← 이 한 줄 추가!   
    CORS(app)
    Swagger(app)

    # DB 커넥션 풀 초기화
    init_db_pool()

    from models.user import User

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    @login_manager.user_loader
    def load_user(user_id):
        from msys.database import get_db_connection
        from service.auth_service import AuthService
        from models.user import User
        
        conn = get_db_connection()
        auth_service = AuthService(conn)
        user_info = auth_service.get_user_by_id(user_id)
        if user_info:
            # 'permissions' 키가 없을 경우를 대비하여 기본값으로 빈 리스트를 사용
            permissions = user_info.get('permissions', [])
            return User(user_id=user_info['user_id'], permissions=permissions)
        return None

    # 세션 사용을 위한 시크릿 키 설정
    app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your_very_secret_key_here')
    # .env에서 관리자 세션 만료 시간(일)을 읽어오고, 없으면 기본값 7일 사용
    # 이 값은 브라우저 쿠키의 최대 수명을 결정합니다.
    admin_session_days = int(os.getenv('ADMIN_SESSION_LIFETIME_DAYS', '7'))
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=admin_session_days)

    # --- 로깅 설정 ---
    log_level = logging.DEBUG if FLASK_DEBUG else logging.INFO

    # IP 주소를 로그에 추가하기 위한 필터
    class RequestContextFilter(logging.Filter):
        def filter(self, record):
            record.remote_addr = request.remote_addr if request else 'N/A'
            return True

    app_log_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(remote_addr)s - %(filename)s:%(lineno)d - %(message)s')
    root_logger = logging.getLogger()
    
    # 기존 핸들러 제거 (중복 출력 방지)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()
        
    root_logger.setLevel(log_level)

    if not FLASK_DEBUG:
        # --- 운영 모드: 파일 로깅 ---
        log_dir = os.getenv('LOG_DIR', 'log')
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # 애플리케이션 로그 파일 핸들러
        app_file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_dir, 'app.log'), when='midnight', backupCount=30, encoding='utf-8'
        )
        app_file_handler.setFormatter(app_log_formatter)
        app_file_handler.addFilter(RequestContextFilter())
        root_logger.addHandler(app_file_handler)

        # Werkzeug (Access) 로그 파일 핸들러
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.setLevel(logging.INFO)
        werkzeug_log_formatter = logging.Formatter('%(asctime)s - %(message)s')
        werkzeug_file_handler = logging.handlers.TimedRotatingFileHandler(
            filename=os.path.join(log_dir, 'access.log'), when='midnight', backupCount=30, encoding='utf-8'
        )
        werkzeug_file_handler.setFormatter(werkzeug_log_formatter)
        werkzeug_logger.addHandler(werkzeug_file_handler)
        werkzeug_logger.propagate = False
        
        app.logger.info("로깅 시스템이 [파일 로깅]으로 초기화되었습니다. (운영 모드)")
    else:
        # --- 개발 모드: 콘솔 로깅 ---
        # 콘솔 핸들러
        # 콘솔 핸들러 (UTF-8 인코딩 명시)
        # sys.stdout.reconfigure(encoding='utf-8') # 이 방법은 일부 환경에서 문제를 일으킬 수 있음
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(app_log_formatter)
        console_handler.addFilter(RequestContextFilter())
        root_logger.addHandler(console_handler)
        
        # Werkzeug 로거도 콘솔에 출력하도록 설정
        werkzeug_logger = logging.getLogger('werkzeug')
        werkzeug_logger.setLevel(logging.INFO)
        werkzeug_logger.addHandler(console_handler)
        werkzeug_logger.propagate = False

        app.logger.info("로깅 시스템이 [콘솔 로깅]으로 초기화되었습니다. (개발 모드)")
    # --- 로깅 설정 종료 ---

    # 애플리케이션 컨텍스트 내에서 DB 매핑 정보 및 메뉴 데이터 초기화
    with app.app_context():
        from msys.column_mapper import column_mapper
        from msys.database import get_db_connection
        from service.mngr_sett_service import MngrSettService
        
        # DB 매핑 정보 초기화
        try:
            conn = get_db_connection()
            column_mapper.init_db_mappings(conn)
        except Exception as e:
            app.logger.error(f"🔥 Failed to initialize ColumnMapper DB mappings: {e}")

        # 메뉴 데이터 캐싱
        try:
            conn = get_db_connection()
            service = MngrSettService(conn)
            app.menu_items = service.get_menu_settings()
            app.logger.info("메뉴 데이터가 성공적으로 캐싱되었습니다.")
        except Exception as e:
            app.logger.error(f"메뉴 데이터 캐싱 실패: {e}")
            app.menu_items = []

    # 블루프린트 초기화
    init_routes(app)

    @app.route('/')
    def index():
        # 이 라우트는 다른 블루프린트가 모두 등록된 후에 정의되어야
        # url_for가 엔드포인트를 올바르게 찾을 수 있습니다.
        return redirect(url_for('dashboard.dashboard'))

    # 요청 종료 시 DB 연결을 닫는 핸들러 등록
    app.teardown_appcontext(close_db_connection)

    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    @app.context_processor
    def inject_menu():
        # 앱 컨텍스트에 캐시된 메뉴 데이터를 사용
        return {'menu_items': app.menu_items}

    @app.context_processor
    def inject_contact_info():
        return {'contact_info': os.getenv('CONTACT_INFO')}

    @app.before_request
    def check_auth():
        # 정적 파일 요청에 대한 로그는 생략하여 로그를 깔끔하게 유지
        if request.path.startswith('/static'):
            return

        app.logger.info(f"--- [AUTH] Checking auth for request: {request.method} {request.path} (Endpoint: {request.endpoint})")
        
        # 세션을 영구 세션으로 설정. PERMANENT_SESSION_LIFETIME에 설정된 시간 후에 만료됩니다.
        session.permanent = True

        if not AUTH_ENABLED:
            g.user = None
            app.logger.info("--- [AUTH] Auth is disabled. Skipping checks.")
            return

        g.user = session.get('user', None)
        app.logger.info(f"--- [AUTH] User in session: {g.user}")

        # Sliding Session: Update expiry time on each request if user is logged in
        if g.user:
            expiry_time_str = session.get('expiry_time')
            app.logger.info(f"--- [AUTH] Found expiry_time in session: {expiry_time_str}")
            
            # expiry_time이 없는 구형 세션은 강제 로그아웃
            if not expiry_time_str:
                session.clear()
                g.user = None
                flash("비정상적인 세션이 감지되어 로그아웃되었습니다. 다시 로그인해주세요.", "warning")
                app.logger.warning("--- [AUTH] Session exists without expiry_time. Forcing re-login.")
                return redirect(url_for('auth.login'))

            try:
                expiry_time = datetime.fromisoformat(expiry_time_str)
                now = datetime.utcnow()
                is_expired = now > expiry_time
                app.logger.info(f"--- [AUTH] Checking session expiry: Now='{now.isoformat()}', Expiry='{expiry_time.isoformat()}', IsExpired={is_expired}")

                if is_expired:
                    session.clear()
                    g.user = None
                    app.logger.info("--- [AUTH] Session expired. Clearing session.")
                    
                    # API 요청에 대해서는 JSON 응답, 그 외에는 로그인 페이지로 리디렉션
                    if request.path.startswith('/api/'):
                        app.logger.warning("--- [AUTH] Unauthorized API access due to session expiration. Returning 401.")
                        return jsonify({"error": "Session expired"}), 401
                    
                    flash("세션이 만료되었습니다. 다시 로그인해주세요.", "warning")
                    app.logger.info("--- [AUTH] Redirecting to login page due to session expiration.")
                    return redirect(url_for('auth.login'))
            except ValueError:
                app.logger.warning(f"--- [AUTH] Invalid expiry_time format: {expiry_time_str}. Forcing re-login.")
                session.clear()
                g.user = None
                flash("비정상적인 세션이 감지되어 로그아웃되었습니다. 다시 로그인해주세요.", "warning")
                return redirect(url_for('auth.login'))

            # 세션 만료 시간 갱신 로직 비활성화
            # new_expiry_time = (datetime.utcnow() + app.config['PERMANENT_SESSION_LIFETIME']).isoformat()
            # session['expiry_time'] = new_expiry_time
            # app.logger.info(f"--- [AUTH] Session expiry time refreshed to: {new_expiry_time}")
        
        if g.user and not g.user.get('user_id'):
            session.clear()
            g.user = None
            flash("비정상적인 세션이 감지되어 로그아웃되었습니다. 다시 로그인해주세요.", "warning")
            app.logger.warning("--- [AUTH] Invalid session detected. Clearing session and redirecting to login.")
            return redirect(url_for('auth.login'))

        excluded_endpoints = ['auth.login', 'auth.logout', 'auth.register', 'auth.request_reset_password', 'static', 'index']

        if g.user:
            app.logger.info(f"--- [AUTH] User is logged in. Checking permissions for path: {request.path}")
            if request.path.startswith('/admin'):
                if 'mngr_sett' not in g.user.get('permissions', []):
                    flash("관리자 권한이 없습니다.")
                    app.logger.warning(f"--- [AUTH] Non-admin user '{g.user.get('user_id')}' tried to access admin path. Redirecting to dashboard.")
                    return redirect(url_for('dashboard.dashboard'))
            app.logger.info("--- [AUTH] Auth check passed for logged-in user.")
            return

        app.logger.info(f"--- [AUTH] User is not logged in. Endpoint is '{request.endpoint}'.")
        if request.endpoint in excluded_endpoints:
            app.logger.info("--- [AUTH] Endpoint is in exclusion list. Allowing access.")
            return

        if request.path.startswith('/api/'):
            app.logger.warning("--- [AUTH] Unauthorized API access attempt. Returning 401.")
            return jsonify({"error": "Authentication required"}), 401
        
        flash("로그인이 필요합니다.")
        app.logger.info("--- [AUTH] No user and not an excluded endpoint. Redirecting to login.")
        return redirect(url_for('auth.login'))

    return app

if __name__ == '__main__':
    app = create_app()
    # .env 파일에서 host와 port를 읽어오고, 없을 경우 기본값을 사용합니다.
    host = os.getenv('FLASK_HOST', 'cib040l5')
    port = int(os.getenv('FLASK_PORT', 18080))
    app.logger.info(f" * Running on http://{host}:{port}")
    app.run(host=host, port=port, debug=FLASK_DEBUG)
