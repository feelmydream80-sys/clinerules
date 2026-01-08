# 데이터 수집 일정 알고리즘 백업 문서

## 문서 정보
- **작성일**: 2026-01-08
- **버전**: 1.0
- **작성자**: AI Assistant (Cline)
- **목적**: collection_schedule 히스토리 매칭 로직 수정 전 백업
- **수정 예정**: 히스토리 처리 로직 제거 (cron 기반 스케줄만 표시)

## 현재 알고리즘 구현 개요

### 1. 주요 컴포넌트
- **서비스**: `service/collection_schedule_service.py`
- **매퍼**: `mapper/mst_mapper.py`, `mapper/dashboard_mapper.py`
- **SQL**: `sql/dashboard/dashboard_sql.py`
- **라우트**: `routes/ui/collection_schedule_routes.py`
- **프론트엔드**: `static/js/pages/collection_schedule.js`

### 2. 알고리즘 흐름

#### 2.1. 메인 메서드: `get_schedule_and_history()`
```python
def get_schedule_and_history(self, start_date, end_date, user: Optional[Dict] = None) -> List[Dict]:
    # 권한 확인 및 MST 데이터 가져오기
    allowed_job_ids = self._get_allowed_job_ids_for_schedule(user)

    # 스케줄 생성
    scheduled_tasks = self._generate_scheduled_tasks(start_date, end_date, allowed_job_ids)

    # 히스토리 데이터 가져오기 및 그룹화
    history_by_date_job = self._fetch_and_group_history_data(start_date, end_date, allowed_job_ids, user)

    # 스케줄과 히스토리 매칭하여 상태 업데이트
    self._match_schedule_with_history(scheduled_tasks, history_by_date_job)

    # 매칭되지 않은 히스토리 처리
    self._process_unmatched_history(scheduled_tasks, history_by_date_job, allowed_job_ids)

    return scheduled_tasks
```

#### 2.2. 스케줄 생성: `_generate_scheduled_tasks()`
- MST에서 cron 스케줄(item6) 조회
- croniter로 기간 내 실행 시간 계산
- 상태: '미수집' 또는 '예정'

#### 2.3. 히스토리 조회: `_fetch_and_group_history_data()`
- TB_CON_HIST에서 실제 실행 기록 조회
- 날짜/Job ID별 그룹화
- KST 변환 및 시간 정보 유지

#### 2.4. 매칭 로직: `_match_schedule_with_history()`
- 스케줄 시간과 히스토리 시간 비교 (5분 허용 오차)
- 매칭 시 상태 업데이트 (성공/실패/미수집)
- 매칭된 히스토리는 제거

#### 2.5. 미매칭 처리: `_process_unmatched_history()`
- 매칭되지 않은 히스토리를 별도 항목으로 추가
- 상태: 실제 실행 상태 유지
- cron: "Unscheduled"

## 과거 이슈 해결 배경

### 1. 문제 발생 (2025년)
데이터 수집 일정 화면에서 **정상 수집된 작업이 '미수집'으로 잘못 표시**되는 심각한 버그 발생.

### 2. 원인 분석
- 스케줄만 표시할 경우 모든 작업이 고정 상태 ('예정'/'미수집')
- 실제 실행 여부가 UI에 반영되지 않음
- 시간 비교 로직 부정확, 날짜 정보 손실 등

### 3. 해결 방안
히스토리 매칭 로직 추가로 예정 스케줄 + 실제 기록 결합 표시.

### 4. 세부 해결 과정
- **1차**: 시간 비교 로직 개선 (5분 허용 오차)
- **2차**: 데이터 조회 함수 변경 (시간 정보 포함)
- **3차**: 최종 로직 수정 (절대 시간 차이 비교)
- **결과**: 정확한 상태 표시 및 매칭되지 않은 기록 별도 표시

## 현재 문제점

### 1. CD1001 2개 표시 현상
- Cron: "0 7 * * *" (하루 1회)
- 히스토리 매칭으로 인한 중복 표시
- 스케줄 1개 + 미매칭 히스토리 1개 = 총 2개

### 2. 요구사항 변경
- 히트맵을 **cron 주기 기반으로만 판단**
- 히스토리 고려하지 않고 스케줄만 표시
- 과거 버그 해결 로직이 현재 불필요

## 수정 계획

### 1. 제거 대상
- `_fetch_and_group_history_data()`
- `_match_schedule_with_history()`
- `_process_unmatched_history()`
- 관련 SQL 쿼리

### 2. 유지 대상
- `_generate_scheduled_tasks()` (스케줄 생성)
- 권한 체크 로직
- MST 조회 로직

### 3. 변경 내용
- 메서드명: `get_schedule_and_history` → `get_schedule_only`
- 반환: 스케줄만 (상태: '예정'/'미수집')
- 히스토리 관련 코드 완전 제거

## 복원 방법

수정 후 문제가 발생할 경우:
1. 이 백업 문서 참고하여 원본 로직 복원
2. `service/collection_schedule_service.py`에 히스토리 메서드 재추가
3. `routes/ui/collection_schedule_routes.py`에서 메서드명 복원
4. 테스트 실행으로 기능 검증

## 참고 자료
- `document/collection_schedule.md`: 과거 이슈 해결 보고서
- `document/technical_debt_log.md`: 기술 부채 로그
- `sql/dashboard/dashboard_sql.py`: 히스토리 조회 SQL