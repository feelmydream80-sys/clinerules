# 화면 구성 도메인 정의 (UI Screen Domain)

**Cline 필수 읽기 문서** — Flask 웹 화면 설계 시 반드시 참조

## 1. 목적
- 각 화면(페이지)의 **도메인(비즈니스 의미)**, **주요 기능**, **필요 데이터**, **상태**를 명확히 정의
- 개발자(Cline 포함)와 기획자 간 화면 이해를 공유
- 화면 구현 시 일반적인 구조와 사용자 경험 유지

## 2. 실제 화면 파일 매핑

| 화면 이름 | URL | 실제 파일 경로 |
|-----------|-----|----------------|
| 감정 분석 (메인) | `/` | `web/templates/index.html` |
| 워드클라우드 | `/wordcloud` | `web/templates/wordcloud.html` |
| 메타데이터 | `/metadata` | `web/templates/metadata.html` |
| 배치 처리 | `/metadata/batch` | `web/templates/metadata_batch.html` |
| 데이터 전처리 | `/preprocess` | `web/templates/preprocess.html` |
| 결과 보기 | `/results` | `web/templates/results.html` |
| 반어법 분석 | `/sarcasm` | `web/templates/sarcasm.html` |
| 불용어 관리 | `/stopwords` | `web/templates/stopwords.html` |
| 설정 | `/settings` | `web/templates/settings.html` |
| 베이스 템플릿 | - | `web/templates/base.html` |

## 3. 화면 정의 템플릿 (새로운 화면 추가 시 반드시 이 형식 사용)

### 화면 이름: [화면 이름]

**URL**: [예: /dashboard 또는 /users]

**실제 파일**: `web/templates/[파일명].html`

**주요 도메인/목적**:
- 이 화면에서 해결하고자 하는 비즈니스 요구사항은 무엇인가?

**주요 기능 (Features)**:
- 목록 표시
- 검색/필터
- 생성/수정/삭제
- 등...

**필요 데이터 (Data Requirements)**:
- 백엔드에서 받아올 데이터 모델 및 필드 목록
- 예: User { id, name, email, created_at, status }

**화면 상태 (States)**:
- 로딩 상태
- 빈 상태 (Empty)
- 에러 상태
- 성공 상태

**관련 API 엔드포인트**:
- GET /api/xxx
- POST /api/xxx 등

**관련 서비스**:
- src/services/xxx_service.py
- src/routes/xxx_routes.py

---

## 시나리오 테스트

### 시나리오: 분석 페이지 워드클라우드 옵션 문제

**상황**: 사용자가 분석 시작 누르면 워드클라우드가 안 생김

**분석 경로**:
1. 00-core.md → "기능 문제 분석/디버깅" → 03.workflow.md
2. 이 문서(screen-domain.md)에서 분석 페이지 파일 확인: `web/templates/index.html`
3. 관련 API 분석: `src/routes/api_routes.py`
4. 관련 서비스: `src/services/wordcloud_service.py`, `src/modules/wordcloud_generator.py`
5. batch_processor.py와 비교하여 옵션 누락 확인

**결과**: ✅ 정확한 파일 경로로 문제 분석 가능

---

### 시나리오: 배치 처리 페이지 디자인 변경

**상황**: 배치 처리 페이지 디자인 개선 요청

**분석 경로**:
1. 00-core.md → "공통 UI/디자인" → 04.design-change.md
2. 이 문서에서 배치 페이지 파일 확인: `web/templates/metadata_batch.html`
3. 현재 디자인 분석 후 변경 계획

**결과**: ✅ 실제 파일 경로로 정확한 안내 가능