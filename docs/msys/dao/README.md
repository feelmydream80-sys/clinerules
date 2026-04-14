# DAO (Data Access Object)

**문서 위치**: `.clinerules/docs/msys/dao/README.md`

## 파일 위치

`dao/` - 데이터베이스 접근 계층

## 역할

SQL 실행, 트랜잭션 관리, 데이터 조회/수정

## 파일 목록

| 파일 | 역할 |
|------|------|
| user_dao.py | 사용자 데이터 접근 |
| analytics_dao.py | 분석 데이터 접근 (접근 로그, 통계) |
| mngr_sett_dao.py | 메뉴 설정 데이터 접근 |
| api_key_mngr_dao.py | API 키 관리 데이터 접근 |
| con_mst_dao.py | 연결 마스터 데이터 접근 |
| con_hist_dao.py | 연결 이력 데이터 접근 |
| mapping_dao.py | 매핑 데이터 접근 |
| icon_dao.py | 아이콘 데이터 접근 |
| data_spec_dao.py | 데이터 사양 접근 |
| trbl_hist_dao.py | 장애 이력 접근 |
| sts_cd_dao.py | 상태 코드 접근 |
| grp_memo_dao.py | 그룹 메모 접근 |
| schedule_settings_dao.py | 일정 설정 접근 |
| sql_loader.py | SQL 로더 유틸리티 |

## service 연동

```
service → dao → database
```

## 관련 문서

- [msys/README.md](../README.md) - 프로젝트 개요
- [services/README.md](../services/README.md) - 서비스 계층
- [mapper/README.md](../mapper/README.md) - SQL 매핑