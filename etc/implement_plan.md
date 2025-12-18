# DB 연결 실패 문제 해결을 위한 이행 계획 문서

## 1. 문제 현상

- Flask 애플리케이션 실행 시 `psycopg2.OperationalError: connection refused` 오류 발생.
- 오류는 특정 기능(`mngr_sett` 관련)을 추가한 코드와 관련이 있으며, 해당 기능의 블루프린트를 비활성화하면 앱이 정상 실행됨.
- 근본 원인은 Flask 앱이 `.env` 파일의 DB 정보를 로드하기 전에, 특정 모듈(아마도 새로 추가된 Service 또는 DAO)이 너무 일찍 DB 연결을 시도하면서 `DB_CONFIG` 값이 `None`이 되기 때문으로 추정됨.

## 2. 진단 및 분석 과정 (완료)

### 2.1. 가설 수립
- **초기 가설:** `MngrSettDAO`의 DB 연결 로직 자체에 문제가 있을 것이다.
- **수정된 가설:** `MngrSettDAO` 자체는 문제가 없으며, Flask 앱의 모듈 로딩 순서 꼬임(순환 참조)으로 인해 DB 정보가 로드되기 전에 DAO가 초기화될 것이다.
- **최종 가설:** `get_schedule_settings`라는 기능을 수행하는 DAO 자체가 존재하지 않았으며, 이로 인해 테스트 과정에서 혼란이 있었다. 진짜 문제는 Flask 앱의 모듈 로딩 순서 문제이다.

### 2.2. 기술 검토 및 독립 테스트 (완료)
- `get_schedule_settings` 및 `update_schedule_settings` 기능을 수행하는 `dao/schedule_settings_dao.py` 파일과 `ScheduleSettingsDAO` 클래스를 신규로 작성함.
- `test_mngr_sett_dao.py` (테스트 파일명은 재사용) 라는 독립 테스트 스크립트를 통해 다음을 검증함:
    1. `.env` 파일로부터 DB 연결 정보를 정상적으로 읽어옴.
    2. `psycopg2`를 통해 DB에 성공적으로 연결함.
    3. `ScheduleSettingsDAO`의 `get` 및 `update` 메소드가 완벽하게 동작함을 확인함 (CRUD 검증 완료).
- **결론:** DB 연결 문제의 원인은 DAO나 DB 설정값이 아닌, Flask 애플리케이션의 **임포트 순서 문제**임이 명백해짐.

## 3. 해결 계획 (진행 예정)

### 3.1. Phase 1: 원인 분석 - 순환 참조 지점 특정
- **목표:** 어떤 `import` 구문이 DB 설정(`my_setting/db_config.py`)보다 먼저 실행되게 만드는지 정확히 찾아낸다.
- **방법:**
    1. `msys_app.py`에서 `mngr_sett_routes` 블루프린트 등록 부분을 다시 활성화하여 오류를 재현한다.
    2. `routes/mngr_sett_routes.py` 부터 시작하여, 의존성 체인을 역으로 추적한다 (`routes` -> `service` -> `dao` / `mapper`).
    3. 각 파일의 상단에 있는 `import` 구문을 하나씩 주석 처리하며 앱을 다시 실행한다.
    4. 어떤 `import` 라인을 주석 처리했을 때 앱이 정상 실행되는지 확인하여, 순환 참조를 유발하는 정확한 지점을 특정한다.

### 3.2. Phase 2: 해결 및 검증
- **목표:** 순환 참조를 해결하고, 애플리케이션이 정상적으로 실행되며 기능도 올바르게 동작하는 것을 확인한다.
- **해결 방안: 지역 임포트(Local Import) 적용**
    - 원인으로 밝혀진 `import` 구문을 파일 상단(전역 범위)에서 제거한다.
    - 해당 모듈이 실제로 필요한 **함수 또는 메소드 내부**에서 `import` 하도록 코드를 수정한다.
    - 이는 모듈의 로딩 시점을 실제 코드가 실행되는 시점까지 지연시켜, 앱 초기화 시점의 의존성 꼬임 문제를 해결하는 가장 안전하고 표준적인 방법이다.
- **검증 절차:**
    1. 코드를 수정한 후, `flask run`으로 애플리케이션을 실행하여 `connection refused` 오류가 사라졌는지 확인한다.
    2. Postman 또는 브라우저를 통해 `schedule_settings` 관련 API를 호출하여 데이터가 정상적으로 조회되고 수정되는지 최종 기능 테스트를 수행한다.

## 4. 소스 변경 내역

| 파일 경로 | 변경 유형 | 변경 사유 |
| --- | --- | --- |
| `dao/schedule_settings_dao.py` | 신규 생성 | `tb_data_clt_schd_sett` 테이블을 위한 DAO 구현. |
| `test_mngr_sett_dao.py` | 신규 생성/수정 | 신규 DAO의 기능(CRUD)을 독립적으로 검증하기 위함. |
| *(이후 해결 과정에서 변경되는 파일들을 여기에 추가할 예정)* | | |