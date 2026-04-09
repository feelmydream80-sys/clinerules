# 관리 페이지 규칙 (Admin Page Rules)

> 이 문서는 00-core.md에서 참조합니다.

## 관리 페이지 규칙 (CRITICAL)
- **모든 관리 페이지는 template-management-page.md를 기준 패턴으로 함**
- 새 관리 페이지 작업 시: **반드시 template-management-page.md 먼저 읽기**
- 기존 관리 페이지 수정 시: 해당 페이지 문서 + template-management-page.md 동시 참조

## 기준 패턴 문서 위치
- `docs/ui/project/domains/right-content/template-management-page.md`

## 관리 페이지 개발 체크리스트
- [ ] template-management-page.md 읽기
- [ ] 대상 페이지 문서 읽기
- [ ] 기준 패턴과 비교하여 차이점 확인
- [ ] 일관성 있는 UI/UX 적용
- [ ] 서버 사이드 페이징 구현
- [ ] 검색 기능 구현 (디바운스 적용)
- [ ] 테스트 실행