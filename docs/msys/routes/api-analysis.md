# Analysis API (analysis_api.py)

## 파일 위치

`routes/api/analysis_api.py` (360줄)

## 역할

분석 REST API - 성공률 추이, 수집 이력, 상태 코드 등

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 기능 |
|------------|--------|------|
| `/api/analytics/success_rate_trend` | GET | 성공률 추이 |
| `/api/analytics/collection_history` | GET | 수집 이력 |
| `/api/analytics/status_codes` | GET | 상태 코드 조회 |
| `/api/analytics/job_summary` | GET | Job 요약 데이터 |
| `/api/analytics/heatmap` | GET | 히트맵 데이터 |

## 권한

- `login_required` - 로그인 필수
- `check_password_change_required` - 비밀번호 변경 강제
- `analysis_required` - analysis 권한
- `data_analysis_required` - data_analysis 권한

## 의존성

- `service/dashboard_service.py` - 대시보드 서비스
- `service/mst_service.py` - 마스터 서비스
- `service/analysis_service.py` - 분석 서비스
- `service/status_code_service.py` - 상태 코드 서비스
- `dao/analytics_dao.py` - 분석 DAO

## 관련 문서

- [routes/README.md](README.md) - routes 개요
- [routes/analysis-routes.md](analysis-routes.md) - 분석 라우트
- [services/analysis-service.md](../services/analysis-service.md) - 분석 서비스