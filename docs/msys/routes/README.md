# Routes (라우트)

**문서 위치**: `.clinerules/docs/msys/routes/README.md`

## 파일 위치

`routes/` - Flask Blueprint + 엔드포인트 정의

## 역할

HTTP 요청을 받아对应的 service를 호출하고, JSON 또는 HTML 응답을 반환합니다.

## 파일 목록

| 파일 | 역할 |
|------|------|
| admin_routes.py | 관리자 페이지 (메뉴, 통계, 로그 등) |
| auth_routes.py | 인증 (로그인, 로그아웃, 세션 관리) |
| analysis_routes.py | 분석 관련 페이지 |
| today_routes.py | 오늘의 일정 페이지 |
| mngr_sett_routes.py | 메뉴 설정 페이지 |
| mapping_routes.py | 매핑 관리 페이지 |
| jandi_routes.py | 지정 데이터 페이지 |
| data_spec_routes.py | 데이터 사양 페이지 |
| data_report_routes.py | 데이터 리포트 페이지 |
| card_summary_routes.py | 카드 요약 페이지 |
| routes/ui/dashboard_routes.py | 대시보드 페이지 |
| routes/ui/card_summary_routes.py | 카드 요약 (UI) |
| routes/ui/api_key_mngr_routes.py | API 키 관리 (UI) |
| routes/ui/collection_schedule_routes.py | 수집 일정 페이지 |
| routes/api/auth_api.py | 인증 REST API |
| routes/api/dashboard_api.py | 대시보드 REST API |
| routes/api/data_definition_api.py | 데이터 정의 REST API |
| routes/api/card_summary_api.py | 카드 요약 REST API |
| routes/api/api_key_mngr_routes.py | API 키 관리 REST API |
| routes/api/analysis_api.py | 분석 REST API |

## 엔드포인트 그룹

### 페이지 렌더링 (render_template)

| 라우트 | 템플릿 | 기능 |
|--------|--------|------|
| `/` | dashboard.html | 대시보드 |
| `/login` | login.html | 로그인 |
| `/admin` | - | 관리자 (routes/__init__.py) |
| `/admin/menu` | mngr_sett.html | 메뉴 설정 |
| `/mapping` | mapping_management.html | 매핑 관리 |
| `/jandi` | jandi.html | 지정 데이터 |
| `/data/spec` | data_spec.html | 데이터 사양 |
| `/data/report` | data_report.html | 데이터 리포트 |
| `/card/summary` | card_summary.html | 카드 요약 |
| `/schedule` | collection_schedule.html | 수집 일정 |
| `/api-key` | api_key_mngr.html | API 키 관리 |

### REST API (/api)

| 엔드포인트 | 메서드 | 기능 |
|------------|--------|------|
| `/api/auth/login` | POST | 로그인 |
| `/api/auth/logout` | POST | 로그아웃 |
| `/api/dashboard/stats` | GET | 대시보드 통계 |
| `/api/dashboard/data` | GET | 대시보드 데이터 |
| `/api/data/definition` | GET/POST | 데이터 정의 |
| `/api/card/summary` | GET | 카드 요약 |
| `/api/key/mngr` | GET/POST/PUT/DELETE | API 키 관리 |
| `/api/analysis` | GET/POST | 분석 |

## service 연동

| routes 파일 | 호출 service |
|-------------|-------------|
| admin_routes.py | DashboardService, MngrSettDAO |
| auth_routes.py | AuthService, UserService |
| dashboard_routes.py | DashboardService |
| api_key_mngr_routes.py | ApiKeyMngrService |
| mngr_sett_routes.py | MngrSettService |
| mail_scheduler_service.py | MailSchedulerService |

## 관련 문서

- [msys/README.md](../README.md) - 프로젝트 개요
- [services/README.md](../services/README.md) - 비즈니스 로직
- [templates/screen-domain.md](../templates/screen-domain.md) - 화면-템플릿 매핑