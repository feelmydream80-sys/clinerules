# 🌱 잔디 메뉴 상세 문서

## 🎯 메뉴 정보
- **메뉴 ID**: `jandi`
- **메뉴 이름**: 잔디
- **URL**: `/jandi`
- **메뉴 순서**: 6
- **메뉴 설명**: GitHub 스타일 히트맵으로 일별 작업 실행 성공 횟수를 시각화하여 작업 수행 패턴을 한눈에 파악

## 🔗 관련 파일 구조

### 백엔드 (Flask)
```
📁 routes/jandi_routes.py
├── @bp.route("/jandi") - 메인 잔디 페이지
├── @bp.route("/api/job-list") - 작업 ID 리스트 API (DataTables 서버 사이드 처리)
├── @bp.route("/api/job_mst_info") - 작업 마스터 정보 조회 API
├── @bp.route("/api/jandi-data") - 히트맵 데이터 API (메인)
└── @bp.route("/api/jandi/raw_data") - 히트맵 원본 데이터 API (별칭)

📁 service/jandi_service.py [NEW]
├── get_daily_job_counts() - 잔디 전용 일별 작업 성공 실행 횟수 조회 (CD901, CD902만 카운트)
└── _get_allowed_job_ids() - 데이터 권한 필터링 (상속)

📁 mapper/jandi_mapper.py [NEW]
└── get_daily_job_counts() - 잔디 전용 일별 작업 성공 기록 매핑

📁 sql/jandi/jandi_sql.py [NEW]
└── get_daily_job_counts() - 잔디 전용 일별 작업 성공 기록 SQL 쿼리 생성 (CD901, CD902 필터링)

📁 service/dashboard_service.py [기존]
├── get_daily_job_counts() - 일반적인 일별 작업 실행 건수 조회 (모든 상태)
└── _get_allowed_job_ids() - 데이터 권한 필터링

📁 mapper/dashboard_mapper.py [기존]
└── get_daily_job_counts() - 일반적인 일별 작업 실행 기록 매핑

📁 sql/dashboard/dashboard_sql.py [기존]
└── get_daily_job_counts() - 일반적인 일별 작업 실행 기록 SQL 쿼리 생성
```

### 프론트엔드 (JavaScript)
```
📁 templates/jandi.html
├── 메인 잔디 히트맵 페이지 템플릿
├── 작업 선택 드롭다운
├── 날짜 범위 선택기
├── 히트맵 캔버스
└── 범례 표시

📁 static/js/pages/jandi.js
├── initJandiPage() - 잔디 페이지 초기화
├── fetchJandiData() - 히트맵 데이터 로드
├── renderJandiChart() - 히트맵 차트 렌더링
├── updateDateRange() - 날짜 범위 업데이트
└── handleJobSelection() - 작업 선택 처리
```

## 📋 데이터베이스 테이블

### 주요 조회 테이블
- **`TB_CON_HIST`** (수집 이력 테이블)
  - **역할**: 작업 실행 성공 기록의 원천 데이터
  - **주요 컬럼**:
    - `job_id` (작업 ID)
    - `start_dt` (실행 시작 일시, KST 변환하여 날짜로 사용)
    - `status` (실행 상태, 성공: 'CD901')
    - `end_dt` (실행 종료 일시)

### 참조 테이블
- **`TB_JOB_MST`** (작업 마스터 테이블)
  - **역할**: 작업 기본 정보 및 권한 관리
  - **주요 컬럼**:
    - `job_id` (작업 ID)
    - `job_nm` (작업명)
    - `use_yn` (사용 여부)

## 🔄 데이터 흐름

### 1. 페이지 로드
```
사용자 → /jandi → templates/jandi.html → static/js/pages/jandi.js
```

### 2. 초기 데이터 로드
```
jandi.js → /api/job-list → ConMstService.get_paged_jobs()
                     ↓
히트맵 초기 로드 → /api/jandi-data → DashboardService.get_daily_job_counts()
```

### 3. 데이터 가공 및 필터링
```
DashboardService.get_daily_job_counts()
    ↓ (사용자 권한 적용)
    ↓ (작업 ID 필터링)
    ↓ (날짜 범위 필터링)
    → dashboard_mapper.get_daily_job_counts()
        → DashboardSQL.get_daily_job_counts()
            → TB_CON_HIST 테이블 조회
                → 성공 상태(status = 'CD901')만 필터링
                → 일별 그룹화 및 카운트
```

### 4. 프론트엔드 렌더링
```
히트맵 데이터 수신 → renderJandiChart()
                     ↓
Chart.js 히트맵 생성 → GitHub 스타일 색상 적용
                     ↓
인터랙션 이벤트 바인딩
```

## 🔐 데이터 권한 및 보안

### 사용자 권한 레벨
- **관리자(Admin)**: 모든 작업 데이터 접근 가능
- **일반 사용자**: `data_permissions`에 정의된 작업만 접근 가능

### 데이터 필터링 로직
```python
# service/dashboard_service.py
def get_daily_job_counts(self, job_id, start_date, end_date, all_data, user):
    allowed_job_ids = None
    if user:
        is_admin = 'mngr_sett' in user.get('permissions', [])
        if not is_admin:
            allowed_job_ids = user.get('data_permissions', [])
            if not allowed_job_ids:
                return []  # 권한 없음
    # 권한 필터 적용하여 데이터 조회
```

## 📊 데이터 로직

### 성공 판단 기준
- **성공 상태 코드**: `status = 'CD901'`
  - `CD901`: 성공 (Success)
  - `CD902`: 진행 중 (In Progress) - 카운트하지 않음
- **실패 상태**: `CD902`(진행 중), `CD903`(실패), `CD905`(데이터 없음) 등 기타 상태
- **히트맵 표시**: 성공한 실행 기록만 카운트하여 히트맵에 표시

### 날짜 처리 로직
```sql
-- KST 변환하여 날짜 추출
(start_dt::timestamp AT TIME ZONE 'Asia/Seoul')::date as date
```

### 데이터 집계 로직
```sql
SELECT
    (start_dt::timestamp AT TIME ZONE 'Asia/Seoul')::date as date,
    COUNT(*) as count
FROM TB_CON_HIST
WHERE status = 'CD901'  -- 성공 상태만 필터링 (CD901: 성공)
  AND job_id = %s       -- 작업 ID 필터링 (선택적)
  AND date >= %s        -- 시작일 필터링 (선택적)
  AND date <= %s        -- 종료일 필터링 (선택적)
GROUP BY date
ORDER BY date
```

## 🎨 UI/UX 특징

### 히트맵 디자인
- **색상 스케마**: GitHub 스타일 (연한 회색 → 진한 초록색)
- **셀 형태**: 사각형 셀, 날짜별 배치
- **인터랙션**: 마우스 호버 시 날짜와 실행 횟수 표시
- **범례**: 실행 횟수별 색상 구분 표시

### 필터링 기능
- **작업 선택**: 드롭다운으로 특정 작업 선택 가능
- **날짜 범위**: 시작일/종료일 선택으로 기간 제한
- **전체 데이터**: 관리자용 전체 데이터 조회 옵션

## ⚠️ 주의사항 및 제약사항

### 데이터 제한
- **권한 기반 필터링**: 일반 사용자는 허용된 작업만 조회 가능
- **성공 상태만 표시**: 실패한 실행은 히트맵에 나타나지 않음
- **최대 조회 기간**: 대량 데이터 방지를 위한 기간 제한 고려

### 성능 고려사항
- **인덱스 활용**: `start_dt`, `job_id`, `status` 컬럼에 인덱스 필요
- **대용량 데이터**: 긴 기간 조회 시 성능 저하 가능성
- **메모리 사용**: 히트맵 렌더링 시 브라우저 메모리 사용량 고려

## 🔧 유지보수 및 확장

### 설정 변경 가능 항목
- **성공 상태 코드**: 현재 'CD901' 고정, 필요시 설정화 가능
- **색상 스케마**: 히트맵 색상 커스터마이징
- **최대 조회 기간**: 성능 최적화를 위한 제한 설정

### 확장 가능 기능
- **실패 히트맵**: 성공과 별도로 실패 기록 히트맵 추가
- **시간대별 분석**: 시간별 세부 패턴 분석
- **비교 기능**: 여러 작업 간 히트맵 비교

## 📝 변경 이력

### v1.0.0 (현재 버전)
- 초기 잔디 메뉴 구현
- 히트맵 기반 성공 패턴 시각화
- 작업별/기간별 필터링 기능

### 주요 변경사항 (최근)
- **성공 판단 로직 개선 및 아키텍처 분리**: 모든 실행 기록 → 성공 상태만 카운트로 변경
  - 변경 이유: 대시보드/데이터 일정 메뉴와의 일관성 확보, 디버깅 편의성 향상
  - 변경 내용:
    - 잔디 전용 파일 구조 생성 (`service/jandi_service.py`, `mapper/jandi_mapper.py`, `sql/jandi/jandi_sql.py`)
    - 성공 상태 필터링: `status = 'CD901'` (CD901: 성공만 카운트, CD902: 진행 중 제외)
    - 기존 `dashboard_sql.py`는 일반적인 조회용으로 유지
  - 영향: 히트맵에 성공한 실행만 표시되어 정확한 성공 패턴 파악 가능, 향후 디버깅 시 혼동 방지

## 🎯 향후 개선 방향

### 단기 개선
- 히트맵 색상 스케마 커스터마이징 기능 추가
- 모바일 반응형 디자인 개선
- 데이터 내보내기 기능 추가

### 장기 개선
- 실시간 히트맵 업데이트 기능
- 머신러닝 기반 패턴 분석 기능
- 팀별/프로젝트별 히트맵 그룹화 기능

---

*본 문서는 잔디 메뉴의 모든 측면을 이해하기 위한 종합 가이드입니다. 향후 소스 코드 수정 시 이 문서를 먼저 참고하여 일관성 있는 개발을 진행해주세요.*
