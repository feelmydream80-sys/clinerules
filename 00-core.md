# 🔴 00-Core Rules (항상 최우선 적용)

> ⚠️ **이 파일은 나침반이다. 구체적 내용은 다른 문서에 있다.**
> **작업 유형을 파악 → 아래 분류표에서 해당 유형 찾기 → 명시된 문서로 이동 → 그 문서 읽기**
> **추측 금지. 모르면 사용자에게 "어느 문서를 봐야 합니까?" 질문**

## 현재 프로젝트
**msys** (통합 관리 시스템)

## 이 파일의 역할: 나침반

- **구체적 내용은 나침반이 다루지 않는다**
- **작업 유형을 분류 → 어떤 문서/파일로 가야 하는지 명시적으로 안내**
- **문제 발생 시 "어떤 파일을 먼저 읽어야 하는지" 구체적으로 제시**
- AI가 "어디를 봐야 하지?"라고 헤맬 때, 길을 알려주는 역할
- **사용자가 명시적으로 요청하지 않아도, AI가 스스로 판단해서 작업을 시작하는 경우에도 반드시 이 나침반을 가장 먼저 확인한다**
- 어떤 이유로든 해당 작업 유형에 해당하면, 예외 없이 지정된 문서를 모두 읽고 진행한다

---

## 작업 유형 분류표 (나침반으로서 구체적 파일까지 안내)

| 작업 유형 | 이동할 문서 | msys 문서 |
|-----------|-------------|------------|
| 공통 UI/디자인 | 04.design-change.md → `read_file` docs/ui/common/ | docs/msys/templates/screen-domain.md |
| 프로젝트 화면 | 04.design-change.md → `read_file` docs/msys/templates/ | `templates/*.html` |
| 관리 페이지 | 04.design-change.md → `read_file` docs/core/admin-page-rules.md | `templates/mngr_sett.html` |
| 백엔드 API | 03.workflow.md → `read_file` docs/msys/routes/ | `routes/*.py`, `service/*.py` |
| 모달/폼 | 04.design-change.md → `read_file` docs/msys/templates/ | `templates/*.html` 내 `<form>`, `<modal>` |
| 데이터/JSON | 03.workflow.md → `read_file` docs/msys/ | `service*.py`, `dao/*.py`, `mapper/*.py` |
| 데이터베이스 / 테이블 / DDL | `read_file docs/development/database-naming-standard.md` | `dao/*.py`, `DDL/*.sql` |
| 리팩토링 | 01.legacy-protection.md FIRST → `read_file` docs/msys/ | 대상 파일 경로 명시 필요 |
| 기능 문제 분석/디버깅/개선 | 03.workflow.md → docs/verification/pipeline-analysis.md | docs/msys/ 참조 |
| Git 작업 | 06.git-rules.md | CR 보고서 생성 + 커밋 메시지 형식 |
| 공통 모듈 수정/추가 | 수정 전 **Glob으로 실제 파일 경로 확인** → 상대 경로 계산 검증 | `static/js/modules/common/` |
| 복구/롤백 | 07.recovery-rules.md | 복구 대상 파일 |

---

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
| 지침 추가/삭제/수정 | [08.guideline-modification.md](08.guideline-modification.md) |
| 관리 페이지 규칙 | [docs/core/admin-page-rules.md](docs/core/admin-page-rules.md) |
| 디자인 변경 경로 | [docs/core/design-change-workflow.md](docs/core/design-change-workflow.md) |
| 질문 규칙 | [docs/core/question-rules.md](docs/core/question-rules.md) |
| 시나리오 모음 | [docs/verification/scenarios/](docs/verification/scenarios/) |
| 공통 모듈 수정/추가 | 03.workflow.md → Glob으로 실제 파일 경로 확인 | `static/js/modules/common/*.js` |

---

항상 "현재 작업 유형이 무엇인가"를 스스로 판단하고, 해당 규칙 파일의 내용을 가장 강하게 반영해서 행동하라!