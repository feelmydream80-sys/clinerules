# Services (서비스)

**문서 위치**: `.clinerules/docs/msys/services/README.md`

## 파일 위치

`service/` - 비즈니스 로직 계층

## 역할

라우트와 DAO 사이에서 데이터 처리, business logic, 트랜잭션 관리

## 파일 목록

| 파일 | 역할 |
|------|------|
| auth_service.py | 인증 (로그인 검증, 세션 관리) |
| password_service.py | 비밀번호 정책 검증, 해시 |
| dashboard_service.py | 대시보드 데이터, 통계, 이벤트 |
| api_key_mngr_service.py | API 키 관리 (CRUD) |
| mail_scheduler_service.py | 메일 스케줄링 (예약 전송) |
| collection_schedule_service.py | 데이터 수집 일정 관리 |
| mngr_sett_service.py | 메뉴 설정 관리 |
| data_definition_service.py | 데이터 정의 관리 |
| data_spec_service.py | 데이터 사양 관리 |
| data_report_service.py | 데이터 리포트 |
| jandi_service.py | 지정 데이터 서비스 |
| mapping_service.py | 매핑 관리 |
| card_summary_service.py | 카드 요약 |
| analysis_service.py | 분석 |
| mst_service.py | 마스터 데이터 |
| icon_service.py | 아이콘 관리 |
| status_code_service.py | 상태 코드 관리 |
| trbl_service.py | 장애 관련 |
| url_analyzer_service.py | URL 분석 |
| user_service.py | 사용자 관리 |

## service 연동 구조

```
routes → service → dao → mapper → database
```

## 의존성

- `dao/*.py` - 데이터 접근
- `mapper/*.py` - SQL 매핑
- `msys/database.py` - DB 연결

## 관련 문서

- [msys/README.md](../README.md) - 프로젝트 개요
- [routes/README.md](../routes/README.md) - 라우트
- [dao/README.md](../dao/README.md) - DAO