# Dashboard UI Routes (dashboard_routes.py)

## 파일 위치

`routes/ui/dashboard_routes.py` (59줄)

## 역할

대시보드 페이지 - 메인 대시보드 렌더링

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 템플릿 | 기능 |
|------------|--------|--------|------|
| `/dashboard` | GET | dashboard.html | 대시보드 페이지 |

## 권한

- `login_required` - 로그인 필수
- `check_password_change_required` - 비밀번호 변경 강제
- `dashboard_required` - dashboard 권한
- `log_menu_access` - 메뉴 접근 로깅

## 의존성

- `dao/analytics_dao.py` - 분석 DAO

## 관련 문서

- [routes/README.md](README.md) - routes 개요
- [services/dashboard-service.md](../services/dashboard-service.md) - 대시보드 서비스
- [templates/screen-domain.md](../templates/screen-domain.md) - 화면-템플릿 매핑