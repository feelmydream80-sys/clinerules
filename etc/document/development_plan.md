# 수집 현황 히트맵 개발 계획

## 1. 백엔드 (Backend)
- [ ] `routes/analysis_routes.py`: 신규 `/analysis/collection-heatmap` 라우트 추가
- [ ] `render_template('collection_heatmap.html')` 반환 로직 구현
- [ ] 신규 메뉴 접근 시 접속 기록을 `tb_user_acs_log`에 삽입하는 로직 추가

## 2. 프론트엔드 (Frontend)
- [ ] `templates/collection_heatmap.html`: `base.html`을 상속받는 신규 템플릿 파일 생성 (목업 기반)
- [ ] `static/js/pages/collection_heatmap.js`: 신규 JavaScript 파일 생성
- [ ] API (`/api/analytics/collection_heatmap`) 호출 로직 구현
- [ ] API 응답 데이터를 기반으로 히트맵 UI 동적 렌더링 로직 구현

## 3. 데이터베이스 및 설정 (Database & Configuration)
- [ ] `DDL/data/tb_menu.csv`: '수집 현황 히트맵' 메뉴 데이터 추가
- [ ] `DDL/tb_menu.sql`: 해당 메뉴 추가 `INSERT` 구문 반영
