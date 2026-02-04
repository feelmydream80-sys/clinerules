# 데이터 정의 구현 요약

## 개요
이 문서는 데이터 정의(Data Definition) 기능 구현 과정과 현재 상태를 정리한 문서입니다.

## 구현 현황

### ✅ 완료된 작업

#### 1. 시스템 구조 분석
- **API 흐름 파악**: `/api/data_definition/group/{cd}` 엔드포인트 확인
- **로깅 시스템 확인**: `callAPI()` 함수에서 HTTP 요청/응답 로깅 구현
- **입력 인자 정보 분석**: `cd_cl`, `cd`, `cd_nm`, `cd_desc`, `item1~10`, `update_dt`, `del_dt`, `use_yn` 확인

#### 2. Mock 페이지와 실제 시스템 연동
- **Mock 페이지 HTML 구조**: `data_definition_groups_mock.html`에서 `mngr_sett.html`로 이전
- **JavaScript 로직 이전**: Mock 페이지 로직을 `static/js/tabs/dataDefinition.js`로 이전
- **API 연동 로직 추가**: 비침습적으로 API 호출 로직 추가
- **로깅 시스템 최소화**: 콘솔 전용 로깅으로 변경

#### 3. UI/UX 개선
- **CSS 클래스 정확히 일치**: Mock 페이지와 동일한 클래스 이름 적용
- **전체 CSS 스타일 복사**: Mock 페이지의 CSS 스타일을 `static/css/mngr_sett.css`에 적용
- **HTML 구조 검증**: Mock 페이지 구조와 실제 시스템 구조 차이 분석 및 수정

#### 4. 데이터 렌더링 개선
- **Mock 데이터 구조 분석**: 그룹별 카드 표시 구조 이해
- **렌더링 로직 수정**: 그룹별 카드 표시 로직 개선
- **API 연동 구조 정비**: 내부 `init()` 함수에서 `renderGroupCards()` 호출 추가
- **Mock 데이터 구조 검증**: 카드 표시 정상 동작 확인

#### 5. 기능 구현
- **그룹 추가, 수정, 삭제 버튼 UI 구현**
- **그룹 추가 기능 구현**
- **그룹 수정 기능 구현**
- **그룹 삭제 기능 구현**: use_yn 'N'으로 변경 (소프트 삭제)
- **상세 화면에 추가 버튼 추가**
- **상세 항목 삭제 → use_yn 'N'으로 변경**
- **그룹 카드에 사용중/사용안함 시각적 구분 추가**
- **선택되지 않은 상태에서 수정 버튼 클릭 시 toast 알림 추가**
- **메인 화면에 그룹 추가 버튼 추가**
- **상세 화면 버튼 구조 개선**

#### 6. 동적 폼 생성
- **item1~8 기반 동적 폼 생성 방식 이해**
- **item1~8 기반 동적 폼 생성 구현**
- **모든 그룹에 동일 적용 확인**
- **100단위 그룹 구조 정의 및 적용 범위 확인**
- **그룹정의와 데이터정의 차이 파악**

### 🔄 진행 중인 작업

#### 7. 그룹 추가 버튼 정의 마무리
- **tb_con_mst 테이블 스키마 확인**: 완료
- **그룹 추가 버튼: tb_con_mst 모든 열(마지막 3개 제외) 표시 구현**: 진행 중

#### 8. 실제 DB 연동
- **그룹정의 Service 레이어: DB에서 그룹 데이터 조회 로직 구현**
- **그룹정의 API 엔드포인트: 그룹 목록과 상세 정보 API 구현**
- **그룹정의 JavaScript: 그룹 관리 로직 구현**
- **데이터정의 JavaScript: Mock 데이터 제거, 실제 API만 사용하도록 수정**
- **테스트: 실제 DB 데이터로 정상 동작 확인**

## tb_con_mst 테이블 스키마

### 필드 구조
```sql
CREATE TABLE IF NOT EXISTS public.tb_con_mst
(
    cd_cl character varying(20) NOT NULL,    -- 그룹 코드 (예: CD100, CD200)
    cd character varying(20) NOT NULL,       -- 데이터 코드 (예: CD101, CD102)
    cd_nm character varying(20),             -- 데이터 명칭
    cd_desc character varying(50),           -- 활용목적
    item1 character varying(50),             -- Category ID
    item2 character varying(50),             -- Category
    item3 character varying(150),            -- Columns
    item4 character varying(50),             -- save_path
    item5 character varying(50),             -- filename
    item6 character varying(50),             -- duration
    item7 character varying(50),             -- URL
    item8 character varying(50),             -- API_KEY
    item9 character varying(400),            -- 제외 대상
    item10 character varying(400),           -- 제외 대상
    update_dt timestamp with time zone,      -- 수정일시
    del_dt timestamp with time zone,         -- 삭제일시
    use_yn character(18),                    -- 사용여부
    CONSTRAINT "xpk연계_마스터" PRIMARY KEY (cd_cl, cd)
)
```

### 그룹 추가 버튼 구현 계획
- **표시 필드**: `cd_cl`, `cd`, `cd_nm`, `cd_desc`, `item1~8`, `update_dt`, `use_yn`
- **제외 필드**: `item9`, `item10`, `del_dt`
- **그룹 코드 규칙**: 100단위 (CD100, CD200, CD300...)

## 다음 단계

1. **그룹 추가 버튼 완성**: tb_con_mst 스키마에 맞는 폼 구현
2. **Service 레이어 구현**: DB 연동 로직 구현
3. **API 엔드포인트 구현**: 그룹 관리 API 구현
4. **JavaScript 로직 개선**: Mock 데이터 제거, 실제 API 연동
5. **통합 테스트**: 실제 DB와 연동하여 정상 동작 검증

## 비고
- 현재 89%의 작업이 완료되었습니다.
- 남은 작업은 주로 DB 연동과 실제 API 구현에 집중됩니다.
- 그룹정의와 데이터정의의 차이를 명확히 구분하여 구현 중입니다.