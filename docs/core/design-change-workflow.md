# 디자인 변경 작업 경로 (Design Change Workflow)

> 이 문서는 00-core.md 및 04.design-change.md에서 참조합니다.
> **상세 작업 흐름**을 다루며, 개요는 04.design-change.md를 참조하세요.

## 디자인 변경 작업 경로 (CRITICAL)

### 1. 분석 단계
- 변경 대상 파일 (HTML, CSS, JavaScript) 분석
- 현재 디자인의 레이아웃 구조, 스타일, 컴포넌트 위치 파악
- 기존 디자인과 요청된 디자인의 차이점 식별

### 2. 계획 단계 (사용자에게 제시)
- **변경 계획**: 구체적인 수정 방안 (수정할 파일, 변경 내용, 반응형 대응)
- **예상 화면**: 수정 전/후 비교 예시 (텍스트 기반)
- **승인 요청**: 사용자에게 계획 제시하고 승인을 요청

### 3. 구현 단계
- 계획에 따라 실제 코드 변경
- 변경된 디자인의 기능 테스트
- 다양한 화면 크기에서 반응형 확인

### 4. 완료 단계
- 변경된 디자인의 구체적인 수정 내용 결과 보고
- 필요한 문서에 변경 사항 업데이트

---

## 시나리오 테스트

### 시나리오: 배치 처리 워드클라우드 옵션 분석 페이지 적용

**상황**: 분석 페이지(index.html)에 배치 처리(batch_processor.py)의 워드클라우드 옵션 적용 요청

**올바른 진행**:
1. 00-core.md → "공통 UI/디자인" → 04.design-change.md
2. docs/ui/common/screen-domain.md에서 화면 파일 경로 확인
3. 현재 분석 페이지 HTML 분석: `web/templates/index.html`
4. batch_processor.py 옵션 분석 (background_color, apply_emotion_colors, remove_profanity, max_words, width, height)
5. index.html에 워드클라우드 설정 카드 추가
6. api_routes.py에서 옵션 수신 및 WordCloudGenerator에 전달

**검토 결과**: ✅ 문서 참조 경로가 명확하여 문제 해결 가능