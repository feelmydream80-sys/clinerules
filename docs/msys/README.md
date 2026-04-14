# msys 프로젝트 문서

**문서 위치**: `.clinerules/docs/msys/README.md`

## 프로젝트 개요

msys는 Flask 기반의 통합 관리 시스템으로, 대시보드, 사용자 관리, 데이터 분석, 메일 스케줄링 등의 기능을 제공합니다.

## 파일 구조

```
msys/
├── routes/              # Flask 라우트 (API 엔드포인트 + 페이지 렌더링)
│   ├── admin_routes.py        # 관리자 페이지
│   ├── auth_routes.py         # 인증 (로그인/로그아웃)
│   ├── ui/                    # UI 페이지 라우트
│   │   ├── dashboard_routes.py
│   │   ├── card_summary_routes.py
│   │   ├── api_key_mngr_routes.py
│   │   └── collection_schedule_routes.py
│   └── api/                   # REST API
│       ├── auth_api.py
│       ├── dashboard_api.py
│       ├── data_definition_api.py
│       └── ...
├── service/             # 비즈니스 로직
│   ├── dashboard_service.py
│   ├── auth_service.py
│   ├── mail_scheduler_service.py
│   ├── api_key_mngr_service.py
│   ├── collection_schedule_service.py
│   └── ...
├── dao/                 # 데이터 접근 계층
│   ├── user_dao.py
│   ├── analytics_dao.py
│   ├── mngr_sett_dao.py
│   └── ...
├── mapper/              # SQL 매핑
│   ├── user_mapper.py
│   ├── dashboard_mapper.py
│   ├── jandi_mapper.py
│   └── ...
├── models/              # 데이터 모델
│   └── user.py
├── templates/           # HTML 템플릿
│   ├── dashboard.html
│   ├── mngr_sett.html
│   ├── login.html
│   └── ...
├── msys/                # 핵심 모듈
│   ├── database.py
│   ├── config.py
│   └── mail_send.py
└── utils/               # 유틸리티
    ├── auth_middleware.py
    ├── logging_config.py
    └── ...
```

## 문서 구조 (나침반)

| 계층 | 문서 | 역할 |
|------|------|------|
| routes | [routes/README.md](routes/README.md) | 엔드포인트 매핑 |
| services | [services/README.md](services/README.md) | 비즈니스 로직 |
| dao | [dao/README.md](dao/README.md) | DB 접근 |
| mapper | [mapper/README.md](mapper/README.md) | SQL 매핑 |
| models | [models/README.md](models/README.md) | 데이터 모델 |
| templates | [templates/screen-domain.md](templates/screen-domain.md) | 화면-템플릿 |

## 작업 유형별 참조

| 작업 유형 | 참조 문서 |
|-----------|-----------|
| UI/디자인 변경 | `templates/screen-domain.md` → 해당 template 분석 |
| API 문제 | `routes/` → 해당 route 파일 → `service/` 추적 |
| 데이터 저장 | `service/` → `dao/` → `mapper/` 추적 |
| 새 메뉴 추가 | `routes/` 패턴 참조 → `templates/` 추가 |

## 관련 규칙

- [00-core.md](../../00-core.md) - 나침반
- [01.legacy-protection.md](../../01.legacy-protection.md) - 레거시 보호
- [03.workflow.md](../../03.workflow.md) - 워크플로우
- [04.design-change.md](../../04.design-change.md) - UI 변경