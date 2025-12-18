#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from msys_app import create_app
from msys.database import get_db_connection
from dao.analytics_dao import AnalyticsDAO
import logging

logging.basicConfig(level=logging.INFO)

try:
    app = create_app()
    with app.app_context():
        conn = get_db_connection()
        dao = AnalyticsDAO(conn)

        print('=== 통계 기능 최종 테스트 ===')

        # 오늘 날짜 데이터 조회 (시스템 기준)
        menu_stats = dao.get_menu_access_stats(view_type='daily', start_date='2025-12-15', end_date='2025-12-15')
        total_stats = dao.get_total_access_stats(view_type='daily', start_date='2025-12-15', end_date='2025-12-15')

        print(f'메뉴 통계 결과: {len(menu_stats)}건')
        if menu_stats:
            for stat in menu_stats:
                print(f'  - {stat["menu_nm"]}: {stat["total_access_count"]}회')

        print(f'전체 통계: 총 {total_stats["total_access_count"]}회, 고유 사용자 {total_stats["unique_user_count"]}명')

        # 최근 데이터 날짜 확인
        recent_date = dao.get_most_recent_data_date()
        print(f'최근 데이터 날짜: {recent_date}')

        print('✅ 통계 DAO 기능 정상 작동 확인!')

except Exception as e:
    print(f'❌ 에러 발생: {e}')
finally:
    if 'conn' in locals():
        conn.close()
