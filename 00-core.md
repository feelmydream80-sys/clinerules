# 🔴 00-Core Rules (항상 최우선 적용)

## Before Starting ANY Task - **MANDATORY CHECKLIST**
- [ ] Read 01.legacy-protection.md (최우선 - Legacy 보호)
- [ ] Read 02.documentation.md (작업 시작 전 반드시 읽기 - 문서 지침)
- [ ] Read related docs/ files (design/, development/, verification/)
- [ ] For UI/design changes: Read 04.design-change.md BEFORE modifying ANY code

## Critical Legacy Protection (절대 위반 불가 - 모든 작업에 적용)
- 기존 정상 동작 legacy 코드와 안정화된 프로덕션 코드는 **어떤 부분도 수정, 삭제, 리팩토링, 스타일 변경, 이동 금지**
- legacy 영역은 읽기만 허용. 새로운 코드는 항상 새 파일/새 모듈에 작성
- legacy 코드를 복사해서 수정하는 행위 절대 금지
- 수정이 불가피하면 즉시 중단하고 사용자에게 정확한 파일과 이유를 보고한 뒤 명시적 승인 받기

## 언제 어떤 규칙을 읽고 적용할 것인가 (분류 지침 - 반드시 준수)
작업 유형에 따라 아래 규칙 파일을 **명확히 구분**해서 우선 적용하라:

**모든 작업 공통**: 
  - 01.legacy-protection.md (최우선 - Legacy 보호)
  - 02.documentation.md (작업 시작 시 반드시 먼저 읽음)

**일반 코드 작성 / 기능 구현 / 버그 수정**:
  - 03.workflow.md (작업 흐름)
  - 관련 design docs 확인 (system-design.md, architecture.md, api-design.md)
  - 관련 development docs 확인 (coding-standards.md, tech-stack.md, setup.md)

**디자인/UI 변경 작업**:
  - **반드시 먼저** 04.design-change.md 전체를 읽고 준수
  - 기존 디자인 파일 분석 → 차이점 식별 → 계획 수립 → 사용자 확인 후 구현

**테스트 / 검증 / 보고 관련**:
  - 05.testing.md를 철저히 따름
  - 테스트 결과는 기능별로 구체적으로 보고

**요구사항 오해 발생 시**:
  - 즉시 인정하고, 어느 규칙/문서를 기반으로 오해했는지 명시
  - 올바른 방향 제안

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