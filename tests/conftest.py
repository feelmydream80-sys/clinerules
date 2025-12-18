import pytest
import sys
import os

# 프로젝트 루트 디렉토리를 sys.path에 추가
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from msys_app import app as flask_app

@pytest.fixture
def app(db_conn):
    """Flask app을 위한 pytest fixture를 생성하고, 테스트에 필요한 초기화를 수행합니다."""
    with flask_app.app_context():
        # 테스트 전에 필요한 초기화 수행
        from msys.column_mapper import column_mapper
        column_mapper.init_db_mappings(db_conn)
    yield flask_app

@pytest.fixture
def client(app):
    """
    Flask app의 테스트 클라이언트를 반환합니다.
    이 클라이언트를 사용하여 API 엔드포인트에 요청을 보낼 수 있습니다.
    """
    return app.test_client()

@pytest.fixture
def db_conn():
    """테스트용 데이터베이스 연결을 위한 fixture"""
    from msys.database import get_db_connection
    conn = get_db_connection()
    try:
        yield conn
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        conn.close()

@pytest.fixture
def app_context(app):
    """애플리케이션 컨텍스트를 생성하는 fixture"""
    with app.app_context():
        yield

@pytest.fixture
def admin_service(db_conn):
    """테스트용 AdminService 인스턴스를 생성하는 fixture"""
    from service.admin_settings_service import AdminService
    return AdminService(db_conn)
