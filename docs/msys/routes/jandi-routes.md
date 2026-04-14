# Jandi Routes (jandi_routes.py)

## 파일 위치

`routes/jandi_routes.py` (92줄)

## 역할

지정 데이터 (Jandi) - Job ID 목록, 마스터 상세정보 조회

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 템플릿 | 기능 |
|------------|--------|--------|------|
| `/jandi` | GET | jandi.html | 지정 데이터 페이지 |

### REST API

| 엔드포인트 | 메서드 | 기능 |
|------------|--------|------|
| `/api/job-list` | GET | Job ID 목록 조회 (DataTables) |
| `/api/job_mst_info` | GET | 마스터 상세정보 조회 |

## 의존성

- `service/mst_service.py` - 마스터 서비스
- `service/jandi_service.py` - 지정 데이터 서비스

## 관련 문서

- [routes/README.md](README.md) - routes 개요
- [services/jandi-service.md](../services/jandi-service.md) - 지정 데이터 서비스
- [templates/screen-domain.md](../templates/screen-domain.md) - 화면-템플릿 매핑