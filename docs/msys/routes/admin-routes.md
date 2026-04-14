# Admin Routes (admin_routes.py)

## 파일 위치

`routes/admin_routes.py` (603줄)

## 역할

관리자 페이지 - 메뉴 설정, 통계, 로그, 데이터 내보내기 등 관리 기능 제공

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 기능 |
|------------|--------|------|
| `/admin/mngr_sett` | GET | 메뉴 설정 페이지 렌더링 |
| `/api/statistics/config` | GET | 통계 필터 설정 (연도, 메뉴 목록) |
| `/api/statistics/recent_date` | GET | 최근 데이터 날짜 조회 |
| `/api/statistics` | GET | 기간별 통계 데이터 (daily/weekly/monthly/comparison) |
| `/api/statistics/export` | GET | 통계 데이터 Excel 내보내기 |
| `/api/menu/settings` | GET/POST | 메뉴 설정 조회/저장 |
| `/api/menu/settings/<id>` | PUT/DELETE | 메뉴 설정 수정/삭제 |
| `/api/access-logs` | GET | 접근 로그 조회 |
| `/api/access-logs/export` | GET | 접근 로그 Excel 내보내기 |
| `/api/dashboard/card/data` | GET | 대시보드 카드 데이터 |
| `/api/dashboard/card/export` | GET | 대시보드 카드 Excel 내보내기 |
| `/api/trbl/hist` | GET | 장애 이력 조회 |
| `/api/con/mst` | GET | 연결 마스터 데이터 조회 |
| `/api/con/mst/add` | POST | 연결 마스터 추가 |
| `/api/con/mst/update` | POST | 연결 마스터 수정 |
| `/api/con/mst/delete` | POST | 연결 마스터 삭제 |

## 주요 함수

| 함수 | 기능 |
|------|------|
| `log_menu_access` | 메뉴 접근 로깅 데코레이터 |
| `mngr_sett_page` | 메뉴 설정 페이지 렌더링 |
| `get_statistics_config` | 통계 설정 데이터 반환 |
| `get_statistics` | 통계 데이터 반환 |
| `export_statistics` | 통계 데이터 Excel 내보내기 |
| `get_access_logs` | 접근 로그 조회 |
| `get_card_data` | 대시보드 카드 데이터 |

## 의존성

- `service/dashboard_service.py` - 대시보드 서비스
- `dao/analytics_dao.py` - 분석 DAO
- `dao/mngr_sett_dao.py` - 메뉴 설정 DAO
- `msys/database.py` - DB 연결

## 관련 문서

- [routes/README.md](README.md) - routes 개요
- [services/dashboard-service.md](../services/dashboard-service.md) - 대시보드 서비스
- [dao/analytics-dao.md](../dao/analytics-dao.md) - 분석 DAO