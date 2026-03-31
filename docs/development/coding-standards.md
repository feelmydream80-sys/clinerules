**Cline 필수 읽기 문서** — Python + Flask

## 1. 기본 규칙 (PEP 8 + Best Practices)
- Black 또는 Ruff로 포맷팅
- Type Hint everywhere (`from __future__ import annotations`)
- Google 스타일 Docstring
- 의미 있는 변수/함수명 사용
- Early return, Guard Clause 적극 활용

## 2. Flask 전용 규칙
- Blueprint 이름은 snake_case
- Route 함수는 명확한 이름 (`get_users`, `create_post` 등)
- Configuration은 `Config` 클래스 상속
- Error handling: try/except 최소화하고 Flask errorhandler 활용

## 3. 파일 크기 제한
- 모든 소스 파일은 **300라인을 초과하지 않도록** 유지한다.
- 파일이 300라인을 넘을 것으로 예상되면, 반드시 모듈화해야 한다.

## 4. 모듈화 원칙
- 하나의 파일이 300라인을 초과하려고 하면, 기능을 분리하여 여러 파일로 쪼갠다.
- 각 파일은 하나의 주요 책임(Single Responsibility)만 가지도록 한다.
- 공통 로직은 별도의 유틸리티 파일이나 헬퍼 모듈로 추출한다.

## 5. 작업 절차
1. 파일을 작성하거나 수정할 때, 최종 라인 수가 300을 넘을지 미리 예상한다.
2. 300라인 초과가 예상되면:
   - 모듈화 계획을 먼저 작성한다. (예: "이 파일을 A.py, B.py, utils.py로 분리하겠습니다")
   - 계획을 사용자에게 제시하고 확인을 받는다.
3. 사용자 확인 없이 300라인을 초과하는 단일 파일을 만들거나 수정하지 않는다.