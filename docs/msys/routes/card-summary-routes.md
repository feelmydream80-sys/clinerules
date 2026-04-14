# Card Summary Routes (card_summary_routes.py)

## 파일 위치

`routes/card_summary_routes.py` (18줄)

## 역할

카드 요약 - 대시보드 카드 데이터 조회

## 주요 엔드포인트

| 엔드포인트 | 메서드 | 템플릿 | 기능 |
|------------|--------|--------|------|
| `/card_summary` | GET | card_summary.html | 카드 요약 페이지 |

## 권한

- `login_required` - 로그인 필수
- `card_summary_required` - card_summary 권한
- `log_menu_access` - 메뉴 접근 로깅

## 의존성

- `service/card_summary_service.py` - 카드 요약 서비스

## 관련 문서

- [routes/README.md](README.md) - routes 개요
- [services/card-summary-service.md](../services/card-summary-service.md) - 카드 요약 서비스
- [templates/screen-domain.md](../templates/screen-domain.md) - 화면-템플릿 매핑