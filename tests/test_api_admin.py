import pytest
import json
from msys.column_mapper import reload_mappings
from flask import g

def test_get_all_admin_settings(client):
    """
    GET /api/admin/settings/all API가 정상적으로 모든 관리자 설정을 반환하는지 테스트합니다.
    """
    # admin 권한으로 로그인했다고 가정하기 위해 세션 설정
    with client.session_transaction() as session:
        session['user'] = {'user_id': 'admin', 'permissions': ['admin']}

    # API 호출
    response = client.get('/api/admin/settings/all')

    # 응답 검증
    assert response.status_code == 200
    assert response.is_json
    
    data = response.get_json()
    assert isinstance(data, list) # 응답 데이터는 리스트 형태여야 합니다.

def test_save_admin_settings(client, db_conn, app_context):
    """
    POST /api/admin/settings/save API가 정상적으로 설정을 저장하는지 테스트합니다.
    """
    # --- 테스트 실행 ---
    try:
        # 테스트용 데이터 준비 (실제 DB에 저장되는 컬럼 포함)
        test_settings = [
            {
                "sett_id": "test_setting_01",
                "CNN_FAILR_THRS_VAL": 99
            }
        ]

        # admin 권한으로 로그인했다고 가정하기 위해 세션 설정
        with client.session_transaction() as session:
            session['user'] = {'user_id': 'admin', 'permissions': ['admin']}

        # API 호출
        response = client.post('/api/admin/settings/save', json=test_settings)

        # 응답 검증
        assert response.status_code == 200
        assert response.is_json
        json_data = response.get_json()
        assert json_data['message'] == "모든 설정이 성공적으로 저장되었습니다."

        # DB 데이터 검증 (표준 컬럼명 'cd'와 'cnn_failr_thrs_val'로 조회)
        with db_conn.cursor() as cursor:
            cursor.execute("SELECT cnn_failr_thrs_val FROM tb_mngr_sett WHERE cd = 'test_setting_01'")
            result = cursor.fetchone()
            assert result is not None
            assert result[0] == 99

    finally:
        # --- 테스트 환경 정리 ---
        # 테스트용으로 추가된 설정 데이터만 삭제합니다.
        with db_conn.cursor() as cursor:
            cursor.execute("DELETE FROM tb_mngr_sett WHERE cd = 'test_setting_01'")
        db_conn.commit()
