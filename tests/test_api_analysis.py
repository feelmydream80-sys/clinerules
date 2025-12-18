import pytest
import json

def test_get_dynamic_chart_data_success(client):
    """
    GET /api/analysis/dynamic-chart API가 유효한 파라미터로 정상 작동하는지 테스트합니다.
    """
    # admin 권한으로 로그인했다고 가정
    with client.session_transaction() as session:
        session['user'] = {'user_id': 'admin', 'permissions': ['admin']}

    # API 호출
    response = client.get('/api/analysis/dynamic-chart', query_string={
        'x_axis': 'date',
        'y_axis': 'success_count',
        'group_by': 'job_id',
        'start_date': '2025-01-01',
        'end_date': '2025-01-31'
    })

    # 응답 검증
    assert response.status_code == 200
    assert response.is_json
    data = response.get_json()
    assert isinstance(data, list)

def test_get_dynamic_chart_data_missing_params(client):
    """
    GET /api/analysis/dynamic-chart API가 필수 파라미터 누락 시 400 에러를 반환하는지 테스트합니다.
    """
    with client.session_transaction() as session:
        session['user'] = {'user_id': 'admin', 'permissions': ['admin']}

    response = client.get('/api/analysis/dynamic-chart', query_string={
        'x_axis': 'date',
        'y_axis': 'success_count',
        # start_date, end_date 누락
    })

    assert response.status_code == 400
    assert response.is_json
    json_data = response.get_json()
    assert 'message' in json_data
    assert '필수 파라미터' in json_data['message']

def test_get_dynamic_chart_data_invalid_params(client):
    """
    GET /api/analysis/dynamic-chart API가 유효하지 않은 파라미터(SQL Injection 시도 등)에 대해 400 에러를 반환하는지 테스트합니다.
    """
    with client.session_transaction() as session:
        session['user'] = {'user_id': 'admin', 'permissions': ['admin']}

    response = client.get('/api/analysis/dynamic-chart', query_string={
        'x_axis': 'invalid_column', # 허용되지 않은 컬럼
        'y_axis': 'success_count',
        'start_date': '2025-01-01',
        'end_date': '2025-01-31'
    })

    assert response.status_code == 400
    assert response.is_json
    json_data = response.get_json()
    assert 'message' in json_data
    assert 'Invalid x_axis' in json_data['message']
