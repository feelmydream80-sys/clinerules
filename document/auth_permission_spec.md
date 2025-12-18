# 조회 권한 시스템 분석 및 설계 문서

## 1. 개요

본 문서는 msys 시스템의 조회 권한 관리 기능에 대한 분석 및 설계 내용을 기술합니다. 시스템은 사용자의 역할과 책임에 따라 접근할 수 있는 메뉴와 조회할 수 있는 데이터 범위를 제어하여, 민감한 정보의 노출을 방지하고 데이터 보안을 강화하는 것을 목표로 합니다.

권한 시스템은 크게 두 가지로 구성됩니다.

-   **메뉴 접근 권한**: 사용자가 시스템 내에서 접근할 수 있는 페이지(메뉴)를 제어합니다.
-   **데이터 접근 권한**: 특정 페이지 내에서 사용자가 조회할 수 있는 데이터의 범위를 `Job ID` 기준으로 제한합니다. 관리자(admin)가 아닌 사용자는 허가된 데이터만 볼 수 있습니다.

## 2. 시스템 아키텍처

권한 시스템은 아래와 같은 계층적 구조로 동작합니다.

1.  **Service Layer** (`*_service.py`):
    -   사용자 요청에 대한 비즈니스 로직을 처리합니다.
    -   현재 로그인된 사용자의 권한(메뉴, 데이터)을 확인하고, 권한에 따라 데이터 조회를 Mapper에 요청합니다.
    -   **주요 파일**: `user_service.py`, `mngr_sett_service.py`, `dashboard_service.py`, `analysis_service.py`

2.  **Mapper Layer** (`*_mapper.py`):
    -   Service Layer의 요청을 받아 실제 데이터베이스와 상호작용하는 SQL 쿼리를 실행합니다.
    -   **주요 파일**: `user_mapper.py`

3.  **SQL Layer** (`sql/**/*.sql`, `*_sql.py`):
    -   실행될 SQL 쿼리를 담고 있습니다.
    -   **주요 파일**: `sql/user/user_sql.py`, `sql/user/find_data_permissions_by_user_id.sql` 등

## 3. 핵심 테이블 설계

### 3.1. 메뉴 접근 권한 테이블

-   **테이블명**: `TB_USER_AUTH_CTRL`
-   **설명**: 사용자별로 접근 가능한 메뉴 ID를 저장하여 메뉴 접근 권한을 관리합니다.

| 컬럼명  | 데이터 타입 | 설명       |
| :------ | :---------- | :--------- |
| `USER_ID` | `VARCHAR`   | 사용자 ID (FK) |
| `MENU_ID` | `VARCHAR`   | 메뉴 ID (FK)   |

### 3.2. 데이터 접근 권한 테이블

-   **테이블명**: `TB_USER_DATA_PERM_AUTH_CTRL`
-   **설명**: 사용자별로 조회 가능한 데이터(`Job ID`)를 저장하여 데이터 접근 권한을 관리합니다.

| 컬럼명  | 데이터 타입 | 설명       |
| :------ | :---------- | :--------- |
| `USER_ID` | `VARCHAR`   | 사용자 ID (FK) |
| `JOB_ID`  | `VARCHAR`   | 작업 ID (FK)   |

## 4. 권한 처리 흐름

### 4.1. 메뉴 접근 권한 처리

1.  사용자가 로그인하면 `auth_service`는 `user_mapper.find_user_permissions`를 호출하여 `TB_USER_AUTH_CTRL` 테이블에서 해당 사용자의 메뉴 권한 목록을 가져옵니다.
2.  가져온 권한 목록은 세션에 저장되며, 사용자가 페이지를 이동할 때마다 서버는 이 정보를 바탕으로 메뉴 접근 가능 여부를 판단합니다.
3.  관리자 페이지(`mngr_sett`)에서 `user_service.update_permissions`를 통해 사용자의 메뉴 권한을 수정할 수 있습니다.

### 4.2. 데이터 접근 권한 처리

1.  **사용자 정보 로드**: 사용자가 데이터 조회를 요청하는 API를 호출하면, 해당 `routes`의 핸들러 함수는 `session.get('user')`를 통해 세션에 저장된 사용자 정보 **딕셔너리**를 로드합니다. 이 딕셔너리에는 `user_id`, `permissions`(메뉴 권한), `data_permissions`(허용된 Job ID 목록)가 포함되어 있습니다.

    ```python
    # 예시: routes/api_routes.py
    user = session.get('user')
    ```

2.  **권한 확인 및 데이터 필터링**: 로드된 사용자 정보를 기반으로 데이터 접근 권한을 확인합니다.
    -   **관리자인 경우**: 사용자의 `permissions`에 `mngr_sett`가 포함되어 있으면 관리자로 간주하여 모든 데이터에 접근할 수 있도록 허용합니다. (필터링 미적용)
    -   **일반 사용자인 경우**: 사용자의 `data_permissions`에 저장된 `Job ID` 목록을 기준으로 조회 범위를 제한합니다. 만약 이 목록이 비어있으면, 데이터가 없는 빈 결과를 반환하여 정보 노출을 원천적으로 차단합니다.

3.  **데이터 조회**: 필터링된 `Job ID` 목록을 `Mapper` 계층에 전달하여, 해당 사용자에게 허용된 데이터만을 데이터베이스에서 조회합니다.

4.  **구현 패턴**:
    -   **라우트 내 직접 처리**: `routes/collection_schedule_routes.py`와 같이 라우트 핸들러 내에서 `user.get('data_permissions', [])`를 직접 사용하여 필터링 로직을 구현합니다.
    -   **헬퍼 함수 활용**: `routes/api_routes.py`의 `_get_allowed_job_ids`와 같이 공통 헬퍼 함수를 두어 권한 확인 로직을 표준화합니다.
    -   **서비스 계층 위임**: `routes/card_summary_routes.py`처럼 사용자 정보 딕셔너리를 `Service` 계층으로 전달하여, 서비스 내부(예: `dashboard_service`)에서 권한 확인 및 데이터 조회를 처리하도록 위임합니다.

## 5. 메뉴별 권한 적용 상세 방안

모든 데이터 조회 기능은 앞서 설명한 **데이터 접근 권한 처리** 흐름을 따릅니다. 각 주요 기능별 구현 방식은 다음과 같습니다.

### 5.1. 상세 데이터 조회 (Raw Data)

-   **파일**: `routes/api_routes.py`
-   **API**: `/api/raw_data`, `/api/detail`
-   **구현**: `_get_allowed_job_ids` 헬퍼 함수를 사용합니다.
    1.  `session.get('user')`로 사용자 정보를 가져옵니다.
    2.  `_get_allowed_job_ids`에 사용자 정보와 클라이언트가 요청한 `job_ids`를 전달합니다.
    3.  헬퍼 함수는 사용자의 `data_permissions`와 요청된 `job_ids`의 교집합을 계산하여 최종적으로 허용된 `Job ID` 목록을 반환합니다.
    4.  이 목록을 `dashboard_service.get_raw_data`로 전달하여 데이터를 조회합니다.

    ```python
    # routes/api_routes.py
    def api_raw_data():
        user = session.get('user')
        requested_job_ids = request.args.get('job_ids')
        
        # 1. 헬퍼 함수로 허용된 Job ID 필터링
        allowed_job_ids = _get_allowed_job_ids(user, requested_job_ids)
        
        # 2. 허용된 ID가 없으면 빈 결과 반환
        if allowed_job_ids is not None and not allowed_job_ids:
            return jsonify([]), 200
            
        # 3. 필터링된 ID로 서비스 호출
        rows = dashboard_service.get_raw_data(job_ids=allowed_job_ids)
        return jsonify(rows)
    ```

### 5.2. 데이터 수집 일정 (Collection Schedule)

-   **파일**: `routes/collection_schedule_routes.py`
-   **API**: `/api/collection_schedule`
-   **구현**: 라우트 핸들러 내에서 직접 권한을 처리합니다.
    1.  `session.get('user')`로 사용자 정보를 가져옵니다.
    2.  사용자가 관리자가 아닌 경우, `user.get('data_permissions', [])`를 통해 허용된 `Job ID` 목록을 `allowed_job_ids` 변수에 할당합니다.
    3.  이 `allowed_job_ids`를 `mst_mapper.get_all_mst_for_schedule` (예정된 작업 목록 조회) 및 `dashboard_service.get_collection_history_for_schedule` (실제 수집 이력 조회) 함수에 전달하여 결과 범위를 제한합니다.

### 5.3. 실시간 현황 (Card Summary) 및 대시보드 (Dashboard)

-   **파일**: `routes/card_summary_routes.py`, `routes/dashboard_routes.py`
-   **구현**: 서비스 계층에 권한 처리를 위임합니다.
    1.  `session.get('user')`로 사용자 정보를 가져와 `CardSummaryService` 또는 `DashboardService`의 메소드로 전달합니다.
    2.  서비스 내부에서는 전달받은 `user` 딕셔너리를 공통 권한 처리 모듈/함수(예: `dashboard_service._get_allowed_job_ids`)로 넘겨 데이터 조회를 수행합니다. 이 방식은 권한 처리 로직의 재사용성을 높입니다.

### 5.4. 데이터 명세서 (Data Spec)

-   데이터 명세서 조회 역시 다른 메뉴와 동일한 방식으로 권한 제어를 적용해야 합니다.
-   `data_spec_service.py`에서 `Job ID`를 기준으로 명세서를 조회하는 모든 메소드는, `user` 정보 딕셔너리를 인자로 받아 허용된 `Job ID` 목록을 확인하고 조회 범위를 필터링해야 합니다.

## 6. 서버 사이드 권한 체크 데코레이터

프론트엔드 메뉴 선택 시 권한 확인 외에, 사용자가 브라우저에서 URL을 직접 입력하여 접근하는 것을 방지하기 위해 서버 사이드에서 추가적인 권한 체크를 구현했습니다.

### 6.1. 데코레이터 구현

`routes/auth_routes.py`에 각 메뉴에 대한 권한 체크 데코레이터를 정의했습니다.

```python
def analysis_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user_permissions = session.get('user', {}).get('permissions', [])
        if 'analysis' not in user_permissions:
            return render_template("unauthorized.html")
        return f(*args, **kwargs)
    return decorated_function
```

### 6.2. 적용된 데코레이터 목록

총 9개의 권한 체크 데코레이터가 구현되어 있습니다:

1. `admin_required` - 관리자 설정 (`mngr_sett`)
2. `collection_schedule_required` - 수집 일정 (`collection_schedule`)
3. `analysis_required` - 차트분석 (`analysis`)
4. `data_analysis_required` - 데이터분석 (`data_analysis`)
5. `card_summary_required` - 카드요약 (`card_summary`)
6. `data_report_required` - 데이터보고 (`data_report`)
7. `data_spec_required` - 데이터명세서 (`data_spec`)
8. `jandi_required` - 잔디현황 (`jandi`)
9. `mapping_required` - 매핑관리 (`mapping`)

### 6.3. 라우트 적용 방식

각 메뉴의 라우트 파일에서 해당 데코레이터를 import하여 적용합니다:

```python
from routes.auth_routes import analysis_required

@analysis_bp.route("/chart_analysis")
@login_required
@analysis_required
@log_menu_access
def chart_analysis():
    return render_template("chart_analysis.html")
```

### 6.4. 보안 효과

- **URL 직접 입력 차단**: 권한이 없는 사용자가 브라우저 주소창에 URL을 입력해도 접근할 수 없음
- **API 보호**: 프론트엔드에서 호출하는 API 엔드포인트도 권한 체크 적용
- **캐시 우회**: 브라우저 캐시로 인한 우회 접근 방지

이러한 서버 사이드 권한 체크는 프론트엔드 권한 확인을 보완하여 시스템의 보안을 강화합니다.
