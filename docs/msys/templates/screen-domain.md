# Screen Domain (화면-템플릿 매핑)

**문서 위치**: `.clinerules/docs/msys/templates/screen-domain.md`

## 파일 위치

`templates/` - Flask HTML 템플릿

## 역할

화면(URL)과 템플릿 파일 매핑 - UI 변경 시 참조

## 화면-템플릿 매핑

| URL | 템플릿 | 라우트 | 기능 |
|-----|--------|--------|------|
| `/login` | login.html | auth_routes.py | 로그인 |
| `/` 또는 `/dashboard` | dashboard.html | dashboard_routes.py | 대시보드 |
| `/chart_analysis` | chart_analysis.html | analysis_routes.py | 차트 분석 |
| `/data_analysis` | data_analysis.html | analysis_routes.py | 데이터 분석 |
| `/admin/mngr_sett` | mngr_sett.html | admin_routes.py | 메뉴 설정 |
| `/mngr_sett_test` | mngr_sett_test.html | mngr_sett_routes.py | 메뉴 설정 테스트 |
| `/mapping` | mapping_management.html | mapping_routes.py | 매핑 관리 |
| `/jandi` | jandi.html | jandi_routes.py | 지정 데이터 |
| `/data/spec` | data_spec.html | data_spec_routes.py | 데이터 사양 |
| `/data/report` | data_report.html | data_report_routes.py | 데이터 리포트 |
| `/card/summary` | card_summary.html | card_summary_routes.py | 카드 요약 |
| `/collection_schedule` | collection_schedule.html | collection_schedule_routes.py | 수집 일정 |
| `/api_key_mngr` | api_key_mngr.html | api_key_mngr_routes.py | API 키 관리 |
| `/change-password` | change_password.html | auth_routes.py | 비밀번호 변경 |
| - | unauthorized.html | - | 권한 없음 페이지 |
| - | base.html | - | 기본 레이아웃 |
| - | navbar.html | - | 네비게이션 바 |

## 템플릿 구조

```
templates/
├── base.html          # 기본 레이아웃 (header, footer 포함)
├── navbar.html        # 네비게이션
├── login.html         # 로그인
├── dashboard.html     # 대시보드
├── mngr_sett.html     # 메뉴 설정
├── mapping_management.html  # 매핑 관리
├── jandi.html         # 지정 데이터
├── data_spec.html     # 데이터 사양
├── data_report.html   # 데이터 리포트
├── card_summary.html # 카드 요약
├── collection_schedule.html # 수집 일정
├── api_key_mngr.html  # API 키 관리
└── change_password.html  # 비밀번호 변경
```

## UI 변경 시 참조

1. **템플릿 수정**: `templates/*.html` 분석
2. **CSS/JS 수정**: `static/` 폴더 확인
3. **라우트 수정**: `routes/` 파일 확인

## 관련 문서

- [msys/README.md](../README.md) - 프로젝트 개요
- [routes/README.md](../routes/README.md) - 라우트
- [04.design-change.md](../../04.design-change.md) - UI 변경 규칙