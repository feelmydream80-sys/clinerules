# 데이터 수집 일정 알고리즘 백업 문서

## 문서 정보
- **작성일**: 2026-01-08
- **버전**: 1.1
- **작성자**: AI Assistant (Cline)
- **목적**: collection_schedule 현재 구현 백업
- **현재 상태**: 히스토리 매칭 유지, 동적 상태 매핑 적용

## 현재 알고리즘 구현 개요

### 1. 주요 컴포넌트
- **서비스**: `service/collection_schedule_service.py`
- **매퍼**: `mapper/mst_mapper.py`, `mapper/dashboard_mapper.py`
- **SQL**: `sql/dashboard/dashboard_sql.py`
- **라우트**: `routes/ui/collection_schedule_routes.py`
- **프론트엔드**: `static/js/pages/collection_schedule.js`

### 2. 알고리즘 흐름

#### 2.1. 메인 메서드: `get_schedule_only()`
```python
def get_schedule_only(self, start_date, end_date, user: Optional[Dict] = None) -> List[Dict]:
    # 권한 확인 및 MST 데이터 가져오기
    allowed_job_ids = self._get_allowed_job_ids_for_schedule(user)

    # 스케줄 생성
    scheduled_tasks = self._generate_scheduled_tasks(start_date, end_date, allowed_job_ids)

    # 히스토리 데이터 가져오기 및 그룹화
    history_by_date_job = self._fetch_and_group_history_data(start_date, end_date, allowed_job_ids, user)

    # 스케줄과 히스토리 매칭하여 상태 업데이트
    self._match_schedule_with_history(scheduled_tasks, history_by_date_job)

    return scheduled_tasks
```

#### 2.2. 스케줄 생성: `_generate_scheduled_tasks()`
- MST에서 cron 스케줄(item6) 조회
- croniter로 기간 내 실행 시간 계산
- 초기 상태: '미수집' 또는 '예정'

#### 2.3. 히스토리 조회: `_fetch_and_group_history_data()`
- TB_CON_HIST에서 실제 실행 기록 조회
- 날짜/Job ID별 그룹화
- KST 변환 및 시간 정보 유지

#### 2.4. 매칭 로직: `_match_schedule_with_history()`
- 스케줄 시간과 히스토리 시간 비교 (5분 허용 오차)
- 매칭 시 하드코딩된 상태 매핑으로 업데이트:
  ```python
  status_mapping = {
      'CD901': '성공',
      'CD902': '실패',
      'CD903': '데이터 존재안함',
      'CD904': '진행중',
      'CD905': '진행중'
  }
  ```
- 매칭된 히스토리는 제거

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

## 현재 구현 상태

### 1. 히스토리 매칭 유지
- 스케줄 생성 후 실제 실행 기록과 매칭하여 상태 업데이트
- 정확한 상태 표시를 위해 히스토리 매칭 로직 유지
- CD1001 중복 표시 문제는 해결됨 (매칭되지 않은 히스토리 별도 표시하지 않음)

### 2. 상태 매핑
- 하드코딩된 상태 매핑 사용:
  - CD901 → '성공'
  - CD902 → '실패'
  - CD903 → '데이터 존재안함'
  - CD904 → '진행중'
  - CD905 → '진행중'
- 향후 DB 동적 조회로 개선 가능

### 3. 카드 요약 연동
- CollectionScheduleService의 상태를 CardSummaryService에서 사용
- 상태별 카테고리 분류: 성공/실패/진행중/미수집/예정

## 향후 개선 계획

### 1. 상태 매핑 동적화
- `sql/mst/get_error_code_map.sql`에 `cd_nm` 추가
- 하드코딩된 매핑을 DB 조회로 대체
- 코드 유지보수성 향상

### 2. 성능 최적화
- 히스토리 조회 쿼리 최적화
- 불필요한 데이터 변환 최소화

### 3. 코드 정리
- 중복 로직 제거
- 메서드 분리 및 책임 명확화

## 구현 노트

현재 구현은 다음과 같은 특징을 가짐:
- `get_schedule_only()` 메서드는 이름과 달리 히스토리 매칭을 수행
- 상태 매핑은 하드코딩되어 있지만 향후 DB 동적화 예정
- 카드 요약 기능과 연동되어 상태별 통계 제공
- 사용자 권한에 따른 Job 필터링 지원

## 테스트 및 검증

현재 구현 검증:
1. 스케줄 생성 정상 작동 확인
2. 히스토리 매칭으로 상태 업데이트 확인
3. 카드 요약에서 상태별 분류 확인
4. API 500 오류 없음 확인

## 참고 자료
- `document/collection_schedule.md`: 과거 이슈 해결 보고서
- `document/technical_debt_log.md`: 기술 부채 로그
- `sql/dashboard/dashboard_sql.py`: 히스토리 조회 SQL