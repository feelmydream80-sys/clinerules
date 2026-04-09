# 🔴 00-Core Rules (항상 최우선 적용)

> ⚠️ **이 파일은 나침반이다. 구체적 내용은 다른 문서에 있다.**
> **작업 유형을 파악 → 아래 분류표에서 해당 유형 찾기 → 명시된 문서로 이동 → 그 문서 읽기**
> **추측 금지. 모르면 사용자에게 "어느 문서를 봐야 합니까?" 질문**

## 현재 프로젝트
**project_wordcloud** (워드클라우드 분석 시스템)

## 이 파일의 역할: 나침반

- **구체적 내용은 나침반이 다루지 않는다**
- **작업 유형을 분류 → 어떤 문서/파일로 가야 하는지 명시적으로 안내**
- **문제 발생 시 "어떤 파일을 먼저 읽어야 하는지" 구체적으로 제시**
- AI가 "어디를 봐야 하지?"라고 헤맬 때, 길을 알려주는 역할
- **사용자가 명시적으로 요청하지 않아도, AI가 스스로 판단해서 작업을 시작하는 경우에도 반드시 이 나침반을 가장 먼저 확인한다**
- 어떤 이유로든 해당 작업 유형에 해당하면, 예외 없이 지정된 문서를 모두 읽고 진행한다

## 문서 구조 이해 (CRITICAL - 혼동 금지)

- **공통 지침** (`.clinerules/docs/`): 모든 프로젝트에 적용되는 범용 규칙
  - `design/common/` - 공통 설계 원칙
  - `development/` - 공통 개발 표준 (코딩 컨벤션, 기술 스택, 환경 설정)
  - `ui/common/` - 공통 UI 가이드
  - `verification/` - 공통 검증/분석 절차 (테스트 전략, 코드 리뷰, 파이프라인 분석)
  - `core/` - 핵심 작업 규칙 (Git, 복구, 질문, 관리 페이지 등)
- **프로젝트 지침** (`docs/` 또는 `.clinerules/docs/project_name/`): 특정 프로젝트 전용 규칙
  - 프로젝트별 설계, UI 화면 정의, 도메인 규칙 등
- **00-core.md**: 나침반 역할만 함. 구체적 내용은 위 문서들에 있음
- **하위 문서들도 나침반 역할 병행**: 각 문서는 상위 문서의 구체화이며, 다시 다른 문서를 안내할 수 있음

## BEFORE ANY TASK - YOU MUST DO THESE FIRST

1. [ ] Read 01.legacy-protection.md (CRITICAL - NO EXCEPTIONS)
2. [ ] Read 02.documentation.md (READ FIRST - ALL TASKS)
3. [ ] Read related docs (아래 분류표 참조)
4. [ ] For UI changes: Read 04.design-change.md FIRST

## 작업 유형 분류표 (나침반으로서 구체적 파일까지 안내)

| 작업 유형 | 이동할 문서 | project_wordcloud 문서 |
|-----------|-------------|------------------------|
| 공통 UI/디자인 | 04.design-change.md → `read_file` docs/ui/common/ | docs/project_wordcloud/templates/screen-domain.md |
| 프로젝트 화면 | 04.design-change.md → `read_file` docs/project_wordcloud/templates/ | `web/templates/*.html` |
| 관리 페이지 | 04.design-change.md → `read_file` docs/core/admin-page-rules.md | `web/templates/metadata*.html` |
| 백엔드 API | 03.workflow.md → `read_file` docs/project_wordcloud/routes/ | `src/routes/*.py`, `src/services/*.py` |
| 모달/폼 | 04.design-change.md → `read_file` docs/project_wordcloud/templates/ | `web/templates/*.html` 내 `<form>`, `<modal>` |
| 데이터/JSON | 03.workflow.md → `read_file` docs/project_wordcloud/ | `src/models/*.py`, `src/services/*.py` |
| 데이터베이스 / 테이블 / DDL | `read_file docs/development/database-naming-standard.md` | `src/models/*.py` |
| 리팩토링 | 01.legacy-protection.md FIRST → `read_file` docs/project_wordcloud/ | 대상 파일 경로 명시 필요 |
| 기능 문제 분석/디버깅 | 03.workflow.md → `read_file` docs/verification/pipeline-analysis.md | docs/project_wordcloud/ 참조 |
| Git 작업 | 06.git-rules.md | - |
| 기능 변경/개선 | 03.workflow.md → `read_file` docs/verification/pipeline-analysis.md | docs/project_wordcloud/ 참조 |
| 복구/롤백 | 07.recovery-rules.md | 복구 대상 파일 |

## 요청 분석 규칙 (MANDATORY - 모든 작업에 적용)

- 사용자 요청을 받으면 다음을 먼저 확인:
  1. 이 요청이 "새 기능 추가"인가 "기존 기능 수정/버그 수정"인가?
  2. 에러 메시지가 있는가? 있다면 전체 맥락 확인
  3. 기존에 동작하던 것이 안 되는 것인가, 처음 만드는 것인가?
  4. **요청 대상이 명확한가?** (어떤 파일, 어떤 폴더, 어떤 저장소인지)
- 확인 없이 코드 수정 시작 금지
- **나침반으로서**: 문제를 파악하면 "이 파일들을 확인하세요"라는 구체적 안내 제공

## 실제 사례 기반 교훈 (대화에서 도출한 교훈 - 지속 추가)

- "안 돼요", "작동 안 해요", "에러나요" → 기존 기능 디버깅 우선, 새 기능 구현 금지
- "기능 라이브러리 로드 실패" 에러 발생 시: API 엔드포인트, 모델 필드, 호출 경로 먼저 확인
- **"정렬/필터링/데이터 표시" 문제: SQL 단에서만 멈추지 말고 전체 파이프라인(백엔드→정제→정렬→프론트엔드)을 검증할 것. docs/verification/pipeline-analysis.md 참조**
- **사용자가 문제 위치를 특정해줬으면: 그 위치를 먼저 확인하고, 사용자가 지시한 분석 순서를 따를 것. 성급한 결론 금지**
- **사용자가 "아니다", "잘못됐다"고 하면: 즉시 중단하고 "어떤 부분이 잘못되었는지" 확인할 것. 동일한 실수를 반복하지 말 것**

## 핵심 규칙 문서 위치

| 규칙 | 문서 위치 |
|------|-----------|
| Legacy Protection | [01.legacy-protection.md](01.legacy-protection.md) |
| 문서 가이드 | [02.documentation.md](02.documentation.md) |
| 워크플로우 | [03.workflow.md](03.workflow.md) |
| UI/디자인 변경 | [04.design-change.md](04.design-change.md) |
| 테스트 | [05.testing.md](05.testing.md) |
| Git 작업 | [06.git-rules.md](06.git-rules.md) |
| 복구/롤백 | [07.recovery-rules.md](07.recovery-rules.md) |
| 관리 페이지 규칙 | [docs/core/admin-page-rules.md](docs/core/admin-page-rules.md) |
| 디자인 변경 경로 | [docs/core/design-change-workflow.md](docs/core/design-change-workflow.md) |
| 질문 규칙 | [docs/core/question-rules.md](docs/core/question-rules.md) |

항상 "현재 작업 유형이 무엇인가"를 스스로 판단하고, 해당 규칙 파일의 내용을 가장 강하게 반영해서 행동하라!

---

## 시나리오 테스트 케이스

### 시나리오 1: 워드클라우드 옵션 누락 발견

**상황**: 사용자가 감정 분석 페이지에서 워드클라우드가 생성되지 않음 보고

**올바른 진행 (나침반 역할)**:
1. 00-core.md 확인 → "기능 문제 분석/디버깅" → 03.workflow.md + docs/verification/pipeline-analysis.md
2. 관련 파일 분석: `src/routes/api_routes.py`, `web/templates/index.html`, `src/modules/wordcloud_generator.py`
3. 배치 처리 옵션과 분석 페이지 옵션 비교 (`batch_processor.py` 참조)
4. 차이점 파악 후 수정 계획 수립

**검토 결과**: ✅ 이 규칙대로 진행하면 문제의 근본 원인 파악 가능

---

### 시나리오 2: 배치 처리 UI 변경 요청

**상황**: 사용자가 배치 처리 페이지 디자인 변경 요청

**올바른 진행**:
1. 00-core.md 확인 → "공통 UI/디자인" → 04.design-change.md
2. 04.design-change.md 참조 → docs/ui/common/screen-domain.md + 현재 디자인 상태 확인
3. 변경 파일: `web/templates/metadata_batch.html`, 관련 CSS

**검토 결과**: ✅ 순환 참조 문제 확인 - 04와 docs/core/design-change-workflow.md 중복

---

### 시나리오 3: 새로운 관리 페이지 추가

**상황**: 새 기능 관리 페이지 추가 요청

**올바른 진행**:
1. 00-core.md 확인 → "관리 페이지" → 04.design-change.md → docs/core/admin-page-rules.md
2. template-management-page.md 기준 패턴 확인
3. 새 페이지 문서 작성

**검토 결과**: ✅ 올바른 경로으나 template-management-page.md 실제 파일是否存在 확인 필요