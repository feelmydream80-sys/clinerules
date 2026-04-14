# Mapping Routes (mapping_routes.py)

## 파일 위치

`routes/mapping_routes.py` (108줄)

## 역할

매핑 관리 - Job ID, URL, 아이콘 등 매핑 데이터 관리

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 템플릿 | 기능 |
|------------|--------|--------|------|
| `/mapping` | GET | mapping_management.html | 매핑 관리 페이지 |

### REST API

| 엔드포인트 | 메서드 | 기능 |
|------------|--------|------|
| `/api/mapping/data` | GET | 매핑 데이터 조회 |
| `/api/mapping/data` | POST | 매핑 데이터 저장 |
| `/api/mapping/data` | PUT | 매핑 데이터 수정 |
| `/api/mapping/data` | DELETE | 매핑 데이터 삭제 |
| `/api/mapping/icons` | GET | 아이콘 목록 조회 |

## 권한

- `login_required` - 로그인 필수

## 의존성

- `service/mapping_service.py` - 매핑 서비스
- `dao/analytics_dao.py` - 분석 DAO

## 관련 문서

- [routes/README.md](README.md) - routes 개요
- [services/mapping-service.md](../services/mapping-service.md) - 매핑 서비스
- [templates/screen-domain.md](../templates/screen-domain.md) - 화면-템플릿 매핑