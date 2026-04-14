# Dashboard API (dashboard_api.py)

## 파일 위치

`routes/api/dashboard_api.py` (128줄)

## 역할

대시보드 REST API - 요약 데이터, 트렌드, 이벤트 통계

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 기능 |
|------------|--------|------|
| `/api/dashboard/summary` | GET | 대시보드 요약 데이터 |
| `/api/dashboard/daily_trend` | GET | 일별 트렌드 데이터 |
| `/api/dashboard/event_counts` | GET | 이벤트 통계 |
| `/api/dashboard/con_mst` | GET | 연결 마스터 데이터 |
| `/api/dashboard/menu` | GET | 메뉴 데이터 |
| `/api/dashboard/icon_menu` | GET | 아이콘-메뉴 매핑 |

## 권한

- `login_required` - 로그인 필수
- `check_password_change_required` - 비밀번호 변경 강제

## 의존성

- `service/dashboard_service.py` - 대시보드 서비스
- `utils/datetime_utils.py` - 날짜 유틸리티

## 관련 문서

- [routes/README.md](README.md) - routes 개요
- [routes/ui-dashboard-routes.md](ui-dashboard-routes.md) - 대시보드 UI
- [services/dashboard-service.md](../services/dashboard-service.md) - 대시보드 서비스