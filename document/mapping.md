# 매핑 관리 (Mapping Management)

## 개요

매핑 관리 메뉴는 데이터베이스 테이블 간의 컬럼 매핑 정보를 관리하는 기능을 제공합니다.

## 주요 기능

- 매핑 정보 조회 (모든 매핑, 미매핑 컬럼)
- 새 매핑 추가
- 기존 매핑 업데이트
- 매핑 삭제 (선택적)

## API 엔드포인트

- `GET /mapping/api/all` - 모든 매핑 정보 조회
- `GET /mapping/api/unmapped` - 미매핑 컬럼 조회
- `POST /mapping/api/add` - 새 매핑 추가
- `POST /mapping/api/update` - 매핑 업데이트

## 권한

- `mapping` 권한 필요
- 서버 사이드 권한 체크 데코레이터 적용

## 관련 파일

- `routes/mapping_routes.py`
- `service/mapping_service.py`
- `templates/mapping_management.html`
