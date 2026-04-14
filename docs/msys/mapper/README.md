# Mapper (SQL 매핑)

**문서 위치**: `.clinerules/docs/msys/mapper/README.md`

## 파일 위치

`mapper/` - SQL 쿼리 매핑 계층

## 역할

DAO에서 호출되는 SQL 정의, 쿼리 실행

## 파일 목록

| 파일 | 역할 |
|------|------|
| user_mapper.py | 사용자 SQL |
| dashboard_mapper.py | 대시보드 SQL |
| jandi_mapper.py | 지정 데이터 SQL |
| mapping_mapper.py | 매핑 SQL |
| icon_mapper.py | 아이콘 SQL |
| data_spec_mapper.py | 데이터 사양 SQL |
| mngr_sett_mapper.py | 메뉴 설정 SQL |
| mst_mapper.py | 마스터 데이터 SQL |
| analysis_mapper.py | 분석 SQL |
| trbl_mapper.py | 장애 SQL |
| grp_memo_mapper.py | 그룹 메모 SQL |

## 계층 구조

```
service → dao → mapper → database
         (mapper 호출)
```

## 관련 문서

- [msys/README.md](../README.md) - 프로젝트 개요
- [dao/README.md](../dao/README.md) - DAO 계층
- [services/README.md](../services/README.md) - 서비스 계층