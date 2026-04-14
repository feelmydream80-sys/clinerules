# Auth Routes (auth_routes.py)

## 파일 위치

`routes/auth_routes.py` (492줄)

## 역할

인증 - 로그인, 로그아웃, 세션 관리, 권한 검사

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 기능 |
|------------|--------|------|
| `/login` | GET/POST | 로그인 페이지 + 처리 |
| `/logout` | POST | 로그아웃 |
| `/change-password` | GET/POST | 비밀번호 변경 |
| `/api/auth/check` | GET | 로그인 상태 확인 |

## 권한 데코레이터

| 데코레이터 | 권한 |
|------------|------|
| `login_required` | 로그인 필수 |
| `admin_required` | mngr_sett 권한 |
| `collection_schedule_required` | collection_schedule 권한 |
| `analysis_required` | analysis 권한 |
| `data_analysis_required` | data_analysis 권한 |
| `card_summary_required` | card_summary 권한 |
| `data_report_required` | data_report 권한 |
| `data_spec_required` | data_spec 권한 |
| `jandi_required` | jandi 권한 |
| `mapping_required` | mapping 권한 |
| `api_key_mngr_required` | api_key_mngr 권한 |
| `mngr_sett_required` | mngr_sett 권한 |
| `check_password_change_required` | 비밀번호 변경 강제 |

## 주요 함수

| 함수 | 기능 |
|------|------|
| `login()` | 로그인 처리 + 세션 생성 |
| `logout()` | 로그아웃 + 세션 삭제 |
| `change_password()` | 비밀번호 변경 |
| `verify_user()` | 사용자 검증 |

## 의존성

- `service/auth_service.py` - 인증 서비스
- `service/password_service.py` - 비밀번호 서비스
- `service/dashboard_service.py` - 대시보드 서비스
- `mapper/user_mapper.py` - 사용자 매퍼

## 관련 문서

- [routes/README.md](README.md) - routes 개요
- [services/auth-service.md](../services/auth-service.md) - 인증 서비스
- [services/password-service.md](../services/password-service.md) - 비밀번호 서비스