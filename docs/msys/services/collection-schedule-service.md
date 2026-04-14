# Collection Schedule Service (collection_schedule_service.py)

## 파일 위치

`service/collection_schedule_service.py` (200줄)

## 역할

데이터 수집 일정 - cron 기반 스케줄 생성, 히스토리 매칭, 상태 계산

## 주요 함수

| 함수 | 기능 |
|------|------|
| `get_schedule_only(start_date, end_date, user)` | 스케줄 데이터 조회 |
| `get_schedule_and_history(start_date, end_date, user)` | 스케줄 + 이력 데이터 |
| `_generate_scheduled_tasks(start_date, end_date, job_ids)` | cron 기반 스케줄 생성 |
| `_fetch_and_group_history_data(start_date, end_date, job_ids, user)` | 이력 데이터 조회 |
| `_match_schedule_with_history(scheduled_tasks, history_by_date_job)` | 스케줄-이력 매칭 |

## 데이터 흐름

1. `_get_allowed_job_ids_for_schedule()` - 사용자 권한별 Job 필터링
2. `_generate_scheduled_tasks()` - cron 표현식으로 스케줄 생성
3. `_fetch_and_group_history_data()` - TB_CON_HIST에서 이력 조회
4. `_match_schedule_with_history()` - 상태 계산 (성공/실패/대기/미실행)

## 의존성

- `mapper/mst_mapper.py` - 마스터 데이터 매퍼
- `mapper/user_mapper.py` - 사용자 매퍼
- `mapper/dashboard_mapper.py` - 대시보드 매퍼

## 관련 문서

- [services/README.md](README.md) - services 개요
- [routes/collection-schedule-routes.md](../routes/collection-schedule-routes.md) - 수집 일정 라우트