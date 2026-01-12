# 데이터 명세서 (Data Specification)

## 개요

데이터 명세서 메뉴는 시스템에서 사용하는 외부 데이터(API 등)의 명세를 관리하는 기능을 제공합니다.

## 주요 기능

- 데이터 명세서 생성, 조회, 수정, 삭제 (CRUD)
- URL을 통한 자동 명세서 스크래핑
- 명세서 이름 중복 확인
- Job ID 기반 권한 제어

## API 엔드포인트

- `GET /data_spec` - 명세서 페이지
- `GET /api/data-spec` - 모든 명세서 조회
- `POST /api/data-spec` - 새 명세서 생성
- `PUT /api/data-spec/<id>` - 명세서 수정
- `DELETE /api/data-spec/<id>` - 명세서 삭제
- `POST /api/scrape-spec` - URL 스크래핑
- `GET /api/data-spec/check-name` - 이름 중복 확인

## 권한

- `data_spec` 권한 필요
- 서버 사이드 권한 체크 데코레이터 적용

## 관련 파일

- `routes/data_spec_routes.py`
- `service/data_spec_service.py`
- `templates/data_spec.html`
