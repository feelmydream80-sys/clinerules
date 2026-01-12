# 🚀 MSYS 애플리케이션 배포 가이드

## 📋 개요

본 문서는 MSYS 애플리케이션의 리눅스 서버 배포 시 발생할 수 있는 주요 문제점들과 해결방법을 정리한 문서입니다.

## 🔧 주요 수정사항 (v2.2.0)

### 6. 데이터 접근 권한 체크 강화

**문제**: 일반 사용자가 권한이 없는 Job ID의 데이터를 여러 메뉴에서 조회할 수 있는 보안 취약점 발견

**해결 파일들**:
- `routes/api/__init__.py`: Raw Data API에 user 파라미터 전달 추가
- `routes/analysis_routes.py`: Analysis Raw Data API에 user 파라미터 전달 추가
- `mapper/dashboard_mapper.py`: 이벤트 로그 조회 시 Job ID 필터링 추가
- `service/dashboard_service.py`: 이벤트 로그에 권한 체크 로직 추가
- `service/collection_schedule_service.py`: 남은 기록 처리 시 권한 체크 추가, user 파라미터 전달 추가
- `service/card_summary_service.py`: 실시간 현황에서 권한 체크 추가

**수정 내용**:

1. **이벤트 로그 권한 체크**
   ```python
   # mapper/dashboard_mapper.py
   def get_event_log(self, ..., job_ids: Optional[List[str]] = None):
       if job_ids is not None:
           if not job_ids:
               return []
           # Job ID 필터링 조건 추가
   ```

2. **Raw Data API 권한 체크**
   ```python
   # routes/api/__init__.py
   rows = dashboard_service.get_raw_data(..., job_ids=allowed_job_ids, user=user)
   ```

3. **데이터 수집 일정 권한 체크**
   ```python
   # service/collection_schedule_service.py
   # 남은 기록 처리 시 권한 체크
   allowed_job_set = None if allowed_job_ids is None else set(allowed_job_ids)
   if allowed_job_set is not None and job_id not in allowed_job_set:
       continue
   ```

4. **실시간 현황 권한 체크**
   ```python
   # service/card_summary_service.py
   if allowed_job_ids is not None and job_id not in allowed_job_ids:
       continue
   ```

**영향**: 
- 모든 메뉴에서 데이터 접근 권한이 일관되게 적용됨
- 권한이 없는 Job ID의 데이터는 표시되지 않음
- 보안 취약점 해결

---

### 7. 관리자 설정 Job ID 목록 정렬

**문제**: 데이터 접근 권한 설정에서 허용된 Job ID 목록이 입력 순서대로 표시되어 가독성 저하

**해결 파일들**:
- `sql/user/find_data_permissions_by_user_id.sql`: ORDER BY 추가
- `routes/mngr_sett_routes.py`: API 레벨 정렬 추가
- `service/mngr_sett_service.py`: Service 레벨 정렬 추가

**수정 내용**:
```sql
-- sql/user/find_data_permissions_by_user_id.sql
ORDER BY JOB_ID ASC;
```

```python
# routes/mngr_sett_routes.py
user['job_ids'] = sorted(job_ids) if job_ids else []

# service/mngr_sett_service.py
permitted_job_ids = sorted(permitted_job_ids) if permitted_job_ids else []
```

**영향**: 관리자 설정에서 Job ID 목록이 오름차순으로 정렬되어 표시됨

---

## 🔧 주요 수정사항 (v2.1.0)

### 1. Decimal 타입 JSON 직렬화 문제 해결

**문제**: PostgreSQL에서 반환되는 `Decimal` 타입 값들이 Flask의 `jsonify()`에서 직렬화되지 않아 500 Internal Server Error 발생

**해결 파일**: `service/mngr_sett_service.py`

**수정 내용**:
```python
# Decimal 타입을 float로 변환 (JSON 직렬화 문제 해결)
if hasattr(value, '__class__') and 'Decimal' in str(type(value)):
    from decimal import Decimal
    if isinstance(value, Decimal):
        value = float(value)
```

**영향**: 스케줄 표시 설정 조회 API (`/api/mngr_sett/schedule_settings`) 정상화

---

### 2. SQL 파일 경로 문제 해결

**문제**: Windows 개발환경과 리눅스 배포환경에서 SQL 파일 경로 계산 방식이 달라 `FileNotFoundError` 발생

**해결 파일**: `dao/sql_loader.py`

**수정 내용**:
- 기존: 단일 경로 계산 방식 (`dao/..sql/`)
- 개선: 다중 경로 탐색 방식
  1. 환경변수 기반 (`PROJECT_ROOT`, `APP_ROOT`, `BASE_DIR`)
  2. `PYTHONPATH` 기반 탐색
  3. 현재 작업 디렉토리 기준
  4. 상위 디렉토리 탐색 (최대 5레벨)
  5. 인코딩 호환성 (UTF-8 → CP949 fallback)

**영향**: 모든 SQL 파일 로딩 관련 기능 안정화

---

### 3. 통계 기능 개선

**문제**: 통계 데이터 조회 시 날짜 비교 및 JSON 변환 문제

**해결 파일들**:
- `dao/analytics_dao.py`: 날짜 범위 쿼리 개선
- `service/mngr_sett_service.py`: Decimal 변환 적용
- `static/js/pages/mngr_sett.js`: 날짜 기본값 설정 개선

**수정 내용**:
- 날짜 비교 쿼리 개선 (`ACS_DT >= start_date AND ACS_DT < end_date`)
- 통계 페이지 날짜 기본값을 오늘 날짜로 설정

**영향**: 관리자 설정 → 통계 탭 정상 작동

---

### 4. DAO 레이어 개선

**문제**: 직접 파일 읽기 방식의 일관성 문제

**해결 파일**: `dao/schedule_settings_dao.py`

**수정 내용**:
- 기존: `open('sql/mngr_sett/file.sql')`
- 개선: `from dao.sql_loader import load_sql; load_sql('mngr_sett/file.sql')`

**영향**: SQL 파일 로딩 방식 표준화

---

### 5. JavaScript 디버그 로깅 제어

**문제**: 프로덕션 환경에서 불필요한 console.log 출력으로 성능 저하 및 보안 이슈 발생

**해결 파일**: `static/js/pages/mngr_sett.js`

**수정 내용**:
```javascript
// 디버그 모드 설정 (프로덕션에서는 false로 변경)
const DEBUG_MODE = false;

function debugLog(...args) {
    if (DEBUG_MODE) {
        console.log('[MngrSett]', ...args);
    }
}

// 기존 console.log → debugLog로 변경
// 예: console.log('통계 데이터 로드 시작') → debugLog('통계 데이터 로드 시작')
```

**배포 전 설정**:
```javascript
// 프로덕션 배포 시
const DEBUG_MODE = false; // 이 줄을 false로 설정
```

**영향**: 프로덕션 환경에서 console 로그 출력 방지, 개발 시 디버깅 용이

---

## 🛠️ 배포 전 준비사항

### 환경변수 설정 (권장)

```bash
# 프로젝트 루트 경로 명시 (선택사항)
export PROJECT_ROOT=/var/www/msys
export APP_ROOT=/var/www/msys
export BASE_DIR=/var/www/msys

# Python 경로 설정
export PYTHONPATH=$PROJECT_ROOT:$PYTHONPATH
```

### 파일 권한 확인

```bash
# SQL 파일 권한 확인 및 설정
ls -la /var/www/msys/sql/mngr_sett/
chmod 644 /var/www/msys/sql/mngr_sett/*.sql

# 로그 디렉토리 권한
mkdir -p /var/log/msys
chmod 755 /var/log/msys
```

### Python 패키지 설치

```bash
cd /var/www/msys
pip install -r requirements.txt

# 필수 패키지 확인
python -c "import psycopg2, flask, decimal; print('필수 패키지 설치 완료')"
```

---

## 🔍 배포 후 검증

### 1. SQL 파일 로드 테스트

```bash
cd /var/www/msys
python -c "
from dao.sql_loader import load_sql
try:
    sql = load_sql('mngr_sett/get_schedule_settings.sql')
    print('✅ SQL 파일 로드 성공')
    print(f'길이: {len(sql)}자')
except Exception as e:
    print(f'❌ SQL 파일 로드 실패: {e}')
"
```

### 2. 데이터베이스 연결 테스트

```bash
python -c "
from msys.database import get_db_connection
try:
    conn = get_db_connection()
    with conn.cursor() as cur:
        cur.execute('SELECT 1')
    print('✅ DB 연결 성공')
    conn.close()
except Exception as e:
    print(f'❌ DB 연결 실패: {e}')
"
```

### 3. 주요 API 테스트

```bash
# 스케줄 설정 조회
curl -s http://localhost:18080/api/mngr_sett/schedule_settings | head -5

# 통계 데이터 조회
curl -s "http://localhost:18080/api/statistics?view_type=daily&start_date=2025-12-15&end_date=2025-12-15" | head -5
```

### 4. 웹 인터페이스 테스트

브라우저에서 다음 페이지 접근 확인:
- 관리자 설정 → 데이터 수집 일정 (스케줄 설정 로드)
- 관리자 설정 → 통계 (통계 데이터 표시)

### 5. 데이터 접근 권한 테스트

**테스트 방법**:
1. 일반 사용자 계정(예: Test2)으로 로그인
2. 해당 사용자에게는 특정 Job ID만 권한 부여 (예: CD101, CD102만 허용)
3. 다음 메뉴에서 권한이 없는 Job ID 데이터가 표시되지 않는지 확인:
   - 대시보드 → Job ID별 상세 현황
   - 대시보드 → 이벤트 로그
   - 상세데이터 → 원천데이터
   - 데이터 수집 일정
   - 실시간 현황

**예상 결과**:
- 권한이 없는 Job ID(예: CD303)의 데이터는 어떤 메뉴에서도 표시되지 않아야 함
- 실패 상태든 미수집 상태든 관계없이 필터링되어야 함
- 관리자 설정에서 Job ID 목록이 오름차순으로 정렬되어 표시되어야 함

---

## 🚨 문제 해결 가이드

### FileNotFoundError 발생 시

1. **현재 작업 디렉토리 확인**:
   ```bash
   python -c "import os; print('CWD:', os.getcwd())"
   ```

2. **SQL 파일 존재 확인**:
   ```bash
   find /var/www/msys -name "*.sql" | head -10
   ```

3. **환경변수 설정**:
   ```bash
   export PROJECT_ROOT=/var/www/msys
   ```

### 500 Internal Server Error 발생 시

1. **애플리케이션 로그 확인**:
   ```bash
   tail -f /var/log/msys/app.log
   ```

2. **Decimal 타입 문제 확인**:
   ```python
   # Decimal 값이 있는지 확인
   from dao.schedule_settings_dao import ScheduleSettingsDAO
   dao = ScheduleSettingsDAO(conn)
   result = dao.get_schedule_settings()
   print([k for k, v in result.items() if 'Decimal' in str(type(v))])
   ```

### JSON 직렬화 오류 발생 시

```python
# JSON 변환 테스트
import json
from service.mngr_sett_service import MngrSettService

service = MngrSettService(conn)
result = service.get_schedule_settings_service()
json.dumps(result)  # 성공 시 JSON 변환 가능
```

---

## 📊 버전 히스토리

- **v2.2.0** (2025-12-16)
  - 데이터 접근 권한 체크 강화 (모든 메뉴에 일관 적용)
  - 이벤트 로그, Raw Data, 데이터 수집 일정, 실시간 현황에서 권한 체크 추가
  - 관리자 설정 Job ID 목록 오름차순 정렬

- **v2.1.1** (2025-12-15)
  - JavaScript 디버그 로깅 제어 추가
  - 프로덕션 환경 console.log 출력 방지

- **v2.1.0** (2025-12-15)
  - Decimal 타입 JSON 직렬화 문제 해결
  - SQL 파일 경로 유연성 개선
  - 통계 기능 안정화
  - DAO 레이어 sql_loader 표준화

- **v2.0.0** (2025-12-08)
  - 초기 배포 버전

---

## 👥 담당자

- 개발: AI Assistant
- 배포: 시스템 담당자
- 문의: 개발팀

---

## ⚠️ 중요 알림

배포 전 반드시 개발 환경에서 테스트를 완료하고, 배포 환경에서도 검증 단계를 모두 수행하세요.

**최종 확인**: 모든 API가 정상 응답하고 웹 인터페이스가 정상 작동하는지 확인 후 서비스 오픈하세요.
