# 데이터 분석 (Data Analysis)

## 개요

데이터 분석 메뉴는 수집된 데이터를 분석하고 AI를 활용한 자동 분석 기능을 제공합니다.

## 주요 기능

- 장애 코드 필터링을 통한 데이터 조회
- AI (Gemini)를 활용한 자동 데이터 분석
- 분석 결과 표시 및 저장
- Job ID 및 기간별 필터링

## API 엔드포인트

- `GET /data_analysis` - 데이터 분석 페이지
- `GET /api/analysis/summary` - 분석 요약 데이터
- `GET /api/analysis/trend` - 추이 데이터
- `GET /api/analysis/raw_data` - 원천 데이터
- `POST /api/gemini` - AI 분석 요청

## 권한

- `data_analysis` 권한 필요
- 서버 사이드 권한 체크 데코레이터 적용

## 관련 파일

- `routes/analysis_routes.py`
- `service/analysis_service.py`
- `templates/data_analysis.html`
