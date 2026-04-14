# Data Spec Routes (data_spec_routes.py)

## 파일 위치

`routes/data_spec_routes.py` (159줄)

## 역할

데이터 사양 - DataTables 기반 데이터 관리

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 템플릿 | 기능 |
|------------|--------|--------|------|
| `/data/spec` | GET | data_spec.html | 데이터 사양 페이지 |

### REST API

| 엔드포인트 | 메서드 | 기능 |
|------------|--------|------|
| `/api/data/spec/list` | GET | 데이터 사양 목록 조회 |
| `/api/data/spec/save` | POST | 데이터 사양 저장 |
| `/api/data/spec/<id>` | PUT | 데이터 사양 수정 |
| `/api/data/spec/<id>` | DELETE | 데이터 사양 삭제 |

## 권한

- `login_required` - 로그인 필수
- `data_spec_required` - data_spec 권한

## 의존성

- `service/data_spec_service.py` - 데이터 사양 서비스
- `dao/analytics_dao.py` - 분석 DAO

## 관련 문서

- [routes/README.md](README.md) - routes 개요
- [services/data-spec-service.md](../services/data-spec-service.md) - 데이터 사양 서비스
- [templates/screen-domain.md](../templates/screen-domain.md) - 화면-템플릿 매핑