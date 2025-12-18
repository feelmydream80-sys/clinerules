# 잔디 현황 (Jandi Status)

## 개요

잔디 현황 메뉴는 Github의 활동 그래프처럼 각 Job의 일별 데이터 수집 현황을 히트맵 형태로 시각화하여 보여줍니다.

## 주요 기능

- Job별 일별 수집 현황 히트맵 표시
- 기간별 조회 (주간/월간)
- Job 목록 조회 및 필터링
- 히트맵 색상으로 수집 상태 표현

## API 엔드포인트

- `GET /jandi` - 잔디 현황 페이지
- `GET /api/job-list` - Job 목록 조회
- `GET /api/jandi-data` - 잔디 데이터 조회

## 권한

- `jandi` 권한 필요
- 서버 사이드 권한 체크 데코레이터 적용

## 관련 파일

- `routes/jandi_routes.py`
- `service/jandi_service.py`
- `templates/jandi.html`
