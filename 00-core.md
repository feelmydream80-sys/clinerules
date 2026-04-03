# 🔴 00-Core Rules (항상 최우선 적용)

> ⚠️ **이 파일은 나침반이다. 구체적 내용은 다른 문서에 있다.**
> **작업 유형을 파악 → 아래 분류표에서 해당 유형 찾기 → 명시된 문서로 이동 → 그 문서 읽기**
> **추측 금지. 모르면 사용자에게 "어느 문서를 봐야 합니까?" 질문.**

## 이 파일의 역할: 나침반
- **구체적 내용을 담는 곳이 아님**
- **작업 유형을 분류 → 어떤 문서로 가야 하는지 안내**
- AI가 "어디를 봐야 하지?"라고 헤맬 때, 길을 알려주는 역할

## BEFORE ANY TASK - YOU MUST DO THESE FIRST
1. [ ] Read 01.legacy-protection.md (CRITICAL - NO EXCEPTIONS)
2. [ ] Read 02.documentation.md (READ FIRST - ALL TASKS)
3. [ ] Read related docs (design/, development/, verification/)
4. [ ] For UI changes: Read 04.design-change.md FIRST

## 작업 유형 분류표 (이 파일의 유일한 역할: 길 안내)

| 작업 유형 | 이동할 문서 |
|-----------|-------------|
| 공통 UI/디자인 | 04.design-change.md → `read_file` docs/ui/common/ |
| 프로젝트 화면 (대시보드, 프로젝트 관리) | 04.design-change.md → `read_file` docs/ui/project/domains/right-content/ |
| 관리 페이지 (기능, 템플릿, 프로젝트) | 04.design-change.md → `read_file` docs/ui/project/domains/right-content/template-management-page.md (기준 패턴) |
| 백엔드 API | 03.workflow.md → `read_file` docs/design/project/ + backend/models.py |
| 모달/폼 | 04.design-change.md → `read_file` docs/ui/project/domains/right-content/ |
| 데이터/JSON | 03.workflow.md → `read_file` docs/design/project/ |
| 리팩토링 | 01.legacy-protection.md FIRST → 수정 대상 파일 `read_file` |

## Critical Legacy Protection (절대 위반 불가 - 모든 작업에 적용)
- 기존 정상 동작 legacy 코드와 안정화된 프로덕션 코드는 **어떤 부분도 수정, 삭제, 리팩토링, 스타일 변경, 이동 금지**
- legacy 영역은 읽기만 허용. 새로운 코드는 항상 새 파일/새 모듈에 작성
- legacy 코드를 복사해서 수정하는 행위 절대 금지
- 수정이 불가피하면 즉시 중단하고 사용자에게 정확한 파일과 이유를 보고한 뒤 명시적 승인 받기

## 관리 페이지 규칙 (CRITICAL)
- **모든 관리 페이지는 template-management-page.md를 기준 패턴으로 함**
- 새 관리 페이지 작업 시: **반드시 template-management-page.md 먼저 읽기**
- 기존 관리 페이지 수정 시: 해당 페이지 문서 + template-management-page.md 동시 참조

## 디자인 변경 작업 경로 (CRITICAL)
1. 04.design-change.md 읽기
2. **`read_file docs/ui/project/current-design-state.md`** - 현재 디자인 상태 (04.design-change.md 제6줄 참조)
3. `read_file docs/ui/project/screen-domain.md` - 화면 목록 및 파일 경로 확인
4. 대상 페이지 문서 읽기 (예: feature-management-page.md)
5. 기준 패턴 문서 읽기 (template-management-page.md)

## 요청 불확실 시 질문 규칙 (MANDATORY)
- 사용자 요청을 정확히 파악하지 못하면 **즉시 중단**하고 사용자에게 질문
- 질문 형식:
  ```
  "요청을 명확히 파악하기 위해 확인이 필요합니다.
   이 작업은 [작업 유형]으로 분류되며,
   [문서명]을 참조해야 할 것 같습니다.
   맞습니까? 아니면 다른 문서를 봐야 합니까?"
  ```
- 예시: "기능 관리 페이지 수정 요청 → 관리 페이지 유형 → template-management-page.md를 기준 패턴으로 참조해야 합니다. 맞습니까?"
- **추측해서 진행 금지**

## 요청 분석 규칙 (MANDATORY - 모든 작업에 적용)
- 사용자 요청을 받으면 다음을 먼저 확인:
  1. 이 요청이 "새 기능 추가"인가 "기존 기능 수정/버그 수정"인가?
  2. 에러 메시지가 있는가? 있다면 전체 맥락 확인
  3. 기존에 동작하던 것이 안 되는 것인가, 처음 만드는 것인가?
- 확인 없이 코드 수정 시작 금지

## 실제 사례 기반 교훈 (대화에서 도출한 교훈 - 지속 추가)
- "안 돼요", "작동 안 해요", "에러나요" → 기존 기능 디버깅 우선, 새 기능 구현 금지
- "기능 라이브러리 로드 실패" 에러 발생 시: API 엔드포인트, 모델 필드, 호출 경로 먼저 확인
- "FP와 예상 기간이 하드코딩된 것 같다" → seed_data.py 초기화 값 vs 자동 계산 값 구분하여 설명
- 요청 의도 파악 실패 시: 즉시 중단하고 "이런 의미로 이해했는데 맞습니까?" 확인

## 복구 작업 규칙
- "복구" 또는 "롤백" 요청 시 반드시 범위를 확인 후 실행
- 전체 롤백은 명시적으로 "전체 롤백" 또는 "모두 복구" 라고 요청한 경우에만 허용
- 특정 파일/시점 복구 시 영향 범위를 먼저 보고 후 승인받기

## Documentation Cross-Reference
- [01.legacy-protection.md](01.legacy-protection.md) - Legacy Protection
- [02.documentation.md](02.documentation.md) - Documentation Guide
- [03.workflow.md](03.workflow.md) - Workflow Process
- [04.design-change.md](04.design-change.md) - UI/Design Changes
- [05.testing.md](05.testing.md) - Testing and Reporting

항상 "현재 작업 유형이 무엇인가"를 스스로 판단하고, 해당 규칙 파일의 내용을 가장 강하게 반영해서 행동하라!
