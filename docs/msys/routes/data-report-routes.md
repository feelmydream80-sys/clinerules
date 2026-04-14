# Data Report Routes (data_report_routes.py)

## 파일 위치

`routes/data_report_routes.py` (13줄)

## 역할

데이터 리포트 - 수집 이력 데이터 조회

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 템플릿 | 기능 |
|------------|--------|--------|------|
| `/data/report` | GET | data_report.html | 데이터 리포트 페이지 |

## 의존성

- `service/dashboard_service.py` - 대시보드 서비스
- `mapper/mst_mapper.py` - 마스터 매퍼
- `mapper/user_mapper.py` - 사용자 매퍼

## 관련 문서

- [routes/README.md](README.md) - routes 개요
- [templates/screen-domain.md](../templates/screen-domain.md) - 화면-템플릿 매핑