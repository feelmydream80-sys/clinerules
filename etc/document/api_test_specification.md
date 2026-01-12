# API 테스트 명세서

## 1. 개요

이 문서는 애플리케이션의 모든 API 엔드포인트를 명세하고, 각 API의 기능, 핵심 검증 로직, 그리고 성공/실패 조건을 정의합니다. 이 명세서는 API 기반 통합 테스트 자동화 프로그램을 구축하기 위한 청사진 역할을 합니다.

---

## 2. 테스트 대상 API 목록

### 2.1. `admin_routes.py`

- **`GET /api/admin/settings/all`**
  - **기능 설명:** 모든 관리자 설정 정보를 조회합니다.
  - **핵심 검증 로직:**
    - DB(`tb_mngr_sett`)의 모든 데이터를 조회하여 반환하는지 확인합니다.
    - DB의 표준 컬럼명이 API 응답에서는 레거시 컬럼명으로 올바르게 변환되었는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, JSON 형식의 데이터 반환
    - 실패: HTTP Status 500, 오류 메시지 반환

- **`POST /api/admin/settings/save`**
  - **기능 설명:** 신규 관리자 설정을 추가하거나 기존 설정을 수정합니다.
  - **핵심 검증 로직:**
    - 요청으로 전달된 레거시 컬럼명 JSON 데이터가 DB(`tb_mngr_sett`)에 표준 컬럼명으로 올바르게 `INSERT` 또는 `UPDATE` 되는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, 성공 메시지 반환
    - 실패: HTTP Status 400/500, 오류 메시지 반환

- **`GET /api/admin/settings/export`**
  - **기능 설명:** 모든 관리자 설정을 JSON 파일로 내보냅니다.
  - **핵심 검증 로직:**
    - DB(`tb_mngr_sett`)의 모든 데이터를 조회하여 JSON 형식으로 반환하는지 확인합니다.
    - 응답 헤더의 `Content-Disposition`이 `attachment; filename=admin_settings.json`으로 설정되었는지 확인합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, JSON 파일 다운로드
    - 실패: HTTP Status 500, 오류 메시지 반환

- **`POST /api/admin/settings/import`**
  - **기능 설명:** JSON 파일로부터 관리자 설정을 가져와 DB에 저장합니다.
  - **핵심 검증 로직:**
    - 업로드된 JSON 파일의 데이터가 DB(`tb_mngr_sett`)에 올바르게 `INSERT` 또는 `UPDATE` 되는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, 성공 메시지 반환
    - 실패: HTTP Status 400/500, 오류 메시지 반환

- **`GET /api/admin/icons/all`**
  - **기능 설명:** 모든 아이콘 정보를 조회합니다.
  - **핵심 검증 로직:**
    - DB(`tb_icon`)의 모든 데이터를 조회하여 반환하는지 확인합니다.
    - DB의 표준 컬럼명이 API 응답에서는 레거시 컬럼명으로 올바르게 변환되었는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, JSON 형식의 데이터 반환
    - 실패: HTTP Status 500, 오류 메시지 반환

- **`POST /api/admin/icons/save`**
  - **기능 설명:** 신규 아이콘을 추가하거나 기존 아이콘을 수정합니다.
  - **핵심 검증 로직:**
    - 요청으로 전달된 데이터가 DB(`tb_icon`)에 올바르게 `INSERT` 또는 `UPDATE` 되는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, 성공 메시지 반환
    - 실패: HTTP Status 500, 오류 메시지 반환

- **`DELETE /api/admin/icons/delete/<int:icon_id>`**
  - **기능 설명:** 특정 아이콘을 삭제합니다.
  - **핵심 검증 로직:**
    - 지정된 `icon_id`에 해당하는 데이터가 DB(`tb_icon`)에서 올바르게 `DELETE` 되는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, 성공 메시지 반환
    - 실패: HTTP Status 400/500, 오류 메시지 반환

- **`POST /api/admin/icons/toggle-display`**
  - **기능 설명:** 아이콘의 표시 여부를 토글합니다.
  - **핵심 검증 로직:**
    - 요청으로 전달된 `icon_id`와 `display_yn` 값에 따라 DB(`tb_icon`)의 `ICON_DSP_YN` 컬럼이 올바르게 `UPDATE` 되는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, 성공 메시지 반환
    - 실패: HTTP Status 400/500, 오류 메시지 반환

- **`GET /api/admin/users`**
  - **기능 설명:** 모든 사용자 목록과 권한 정보를 조회합니다.
  - **핵심 검증 로직:**
    - DB에서 모든 사용자 정보와 메뉴 권한 정보를 조회하여 반환하는지 확인합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, JSON 형식의 데이터 반환
    - 실패: HTTP Status 500, 오류 메시지 반환

- **`POST /api/admin/users/approve`**
  - **기능 설명:** 가입 신청한 사용자를 승인합니다.
  - **핵심 검증 로직:**
    - 대상 사용자의 상태가 'APPROVED'로 변경되고, 비밀번호가 초기화되는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, 성공 메시지 반환
    - 실패: HTTP Status 400/500, 오류 메시지 반환

- **`POST /api/admin/users/reject`**
  - **기능 설명:** 가입 신청을 거절하고 사용자 정보를 삭제합니다.
  - **핵심 검증 로직:**
    - 대상 사용자 정보가 DB에서 완전히 삭제되는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, 성공 메시지 반환
    - 실패: HTTP Status 400/500, 오류 메시지 반환

- **`POST /api/admin/users/delete`**
  - **기능 설명:** 등록된 사용자를 삭제합니다.
  - **핵심 검증 로직:**
    - 대상 사용자 정보가 DB에서 완전히 삭제되는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, 성공 메시지 반환
    - 실패: HTTP Status 400/500, 오류 메시지 반환

- **`POST /api/admin/users/reset-password`**
  - **기능 설명:** 사용자 비밀번호를 초기화합니다.
  - **핵심 검증 로직:**
    - 대상 사용자의 비밀번호가 ID와 동일하게 초기화되는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, 성공 메시지 반환
    - 실패: HTTP Status 400/500, 오류 메시지 반환

- **`POST /api/admin/users/permissions`**
  - **기능 설명:** 사용자의 메뉴 접근 권한을 수정합니다.
  - **핵심 검증 로직:**
    - 요청된 `menu_ids`가 해당 사용자의 권한 정보로 DB에 올바르게 반영되는지 검증합니다.
  - **성공/실패 조건:**
    - 성공: HTTP Status 200, 성공 메시지 반환
    - 실패: HTTP Status 400/500, 오류 메시지 반환

### 2.2. `analysis_routes.py`

- **`GET /api/analytics/success_rate_trend`**
- **`GET /api/analytics/trouble_by_code`**
- **`GET /api/analysis/summary`**
- **`GET /api/analysis/trend`**
- **`GET /api/analysis/raw_data`**
- **`GET /api/analysis/job_ids`**
- **`GET /api/analysis/error_codes`**
- **`GET /api/analysis/error_code_map`**

### 2.3. `api_routes.py`

- **`GET /api/min-max-dates`**
- **`GET /api/detail`**
- **`GET /api/mst_list`**
- **`GET /api/job_mst_info`**
- **`GET /api/con_hist_event_log`**
- **`GET /api/raw_data`**
- **`POST /api/gemini`**
- **`POST /api_test_call`**
- **`POST /api/save-event-log`**

### 2.4. `auth_routes.py`

- **`POST /login`**
- **`POST /register`**
- **`POST /change_password`**
- **`POST /request-reset-password`**

### 2.5. `dashboard_routes.py`

- **`GET /api/dashboard/summary`**
- **`GET /api/dashboard/day-stats/<string:date_str>`**
- **`GET /api/dashboard/min-max-dates`**

### 2.6. `data_spec_routes.py`

- **`GET /api/data-spec`**
- **`POST /api/data-spec`**
- **`POST /api/scrape-spec`**
- **`GET /api/data-spec/check-name`**
- **`GET /api/data-spec/<int:spec_id>`**
- **`PUT /api/data-spec/<int:spec_id>`**
- **`DELETE /api/data-spec/<int:spec_id>`**

### 2.7. `jandi_routes.py`

- **`GET /api/job-list`**
- **`GET /api/job_mst_info`**
- **`GET /api/jandi-data`**
- **`GET /api/jandi/raw-data`**

### 2.8. `mapping_routes.py`

- **`GET /mapping/api/all`**
- **`GET /mapping/api/unmapped`**
- **`POST /mapping/api/add`**
- **`POST /mapping/api/update`**
- **`DELETE /mapping/api/delete/<int:mapp_id>`**
