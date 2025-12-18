#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from msys_app import create_app
from msys.database import get_db_connection
import logging

logging.basicConfig(level=logging.INFO)

try:
    app = create_app()
    with app.app_context():
        conn = get_db_connection()
    with conn.cursor() as cur:
        # 최근 데이터 확인
        cur.execute("SELECT ACS_DT::date as access_date, MENU_NM, COUNT(*) as count FROM TB_USER_ACS_LOG WHERE ACS_DT::date >= CURRENT_DATE - INTERVAL '30 days' GROUP BY ACS_DT::date, MENU_NM ORDER BY ACS_DT::date DESC, MENU_NM LIMIT 20")
        results = cur.fetchall()

        print('최근 30일간의 접속 로그:')
        for row in results:
            print(f'{row[0]} | {row[1]} | {row[2]}건')

        # 특정 날짜 데이터 확인
        cur.execute('SELECT COUNT(*) FROM TB_USER_ACS_LOG WHERE ACS_DT::date = %s', ('2025-12-15',))
        count = cur.fetchone()[0]
        print(f'\n2025-12-15 데이터 건수: {count}')

        # 가장 최근 데이터 확인
        cur.execute('SELECT MAX(ACS_DT::date) FROM TB_USER_ACS_LOG')
        max_date = cur.fetchone()[0]
        print(f'가장 최근 데이터 날짜: {max_date}')

        # 오늘 데이터 확인 (admin 사용자)
        cur.execute("SELECT COUNT(*) FROM TB_USER_ACS_LOG WHERE ACS_DT::date = CURRENT_DATE AND USER_ID = 'admin'")
        today_admin_count = cur.fetchone()[0]
        print(f'오늘 admin 사용자 접속 건수: {today_admin_count}')

        # 오늘 전체 데이터 확인
        cur.execute("SELECT COUNT(*) FROM TB_USER_ACS_LOG WHERE ACS_DT::date = CURRENT_DATE")
        today_total_count = cur.fetchone()[0]
        print(f'오늘 전체 접속 건수: {today_total_count}')

        # 실제 CURRENT_DATE 값 확인
        cur.execute("SELECT CURRENT_DATE")
        current_date = cur.fetchone()[0]
        print(f'현재 데이터베이스 날짜: {current_date}')

        # 최근 5건 데이터 확인 (실제 시간순)
        cur.execute("SELECT ACS_DT, USER_ID, MENU_NM FROM TB_USER_ACS_LOG ORDER BY ACS_DT DESC LIMIT 5")
        recent_logs = cur.fetchall()
        print(f'\n최근 5건 접속 로그 (시간순):')
        for log in recent_logs:
            print(f'{log[0]} | {log[1]} | {log[2]}')

        # admin 사용자의 최근 3건 데이터 확인
        cur.execute("SELECT ACS_DT, MENU_NM FROM TB_USER_ACS_LOG WHERE USER_ID = 'admin' ORDER BY ACS_DT DESC LIMIT 3")
        admin_recent_logs = cur.fetchall()
        print(f'\nadmin 사용자의 최근 3건 로그:')
        for log in admin_recent_logs:
            print(f'{log[0]} | {log[1]}')

        # 실제 오늘 기록된 admin 로그 확인 (다른 방식)
        cur.execute("SELECT ACS_DT, MENU_NM FROM TB_USER_ACS_LOG WHERE USER_ID = 'admin' AND ACS_DT >= CURRENT_DATE ORDER BY ACS_DT DESC LIMIT 5")
        admin_today_logs = cur.fetchall()
        print(f'\nadmin 사용자의 오늘 실제 로그 (>= CURRENT_DATE):')
        for log in admin_today_logs:
            print(f'{log[0]} | {log[1]}')

        # 정확한 오늘 날짜 범위로 확인
        cur.execute("SELECT ACS_DT, MENU_NM FROM TB_USER_ACS_LOG WHERE USER_ID = 'admin' AND ACS_DT::date = CURRENT_DATE ORDER BY ACS_DT DESC LIMIT 5")
        admin_today_exact = cur.fetchall()
        print(f'\nadmin 사용자의 정확한 오늘 로그 (ACS_DT::date = CURRENT_DATE):')
        for log in admin_today_exact:
            print(f'{log[0]} | {log[1]}')

        # 가장 최근에 기록된 로그의 날짜 확인
        cur.execute("SELECT MAX(ACS_DT) FROM TB_USER_ACS_LOG")
        max_timestamp = cur.fetchone()[0]
        print(f'\n가장 최근 로그 타임스탬프: {max_timestamp}')

        # CURRENT_DATE와 비교
        cur.execute("SELECT CURRENT_DATE, MAX(ACS_DT)::date, MAX(ACS_DT)::date = CURRENT_DATE as is_today FROM TB_USER_ACS_LOG")
        date_comparison = cur.fetchone()
        print(f'날짜 비교 - CURRENT_DATE: {date_comparison[0]}, MAX_날짜: {date_comparison[1]}, 오늘인가?: {date_comparison[2]}')

        # ACS_DT 필드의 데이터 타입 확인
        cur.execute("SELECT data_type FROM information_schema.columns WHERE table_name = 'tb_user_acs_log' AND column_name = 'acs_dt'")
        acs_dt_type = cur.fetchone()[0]
        print(f'\nACS_DT 필드 타입: {acs_dt_type}')

        # 현재 시간대 확인
        cur.execute("SHOW timezone")
        timezone = cur.fetchone()[0]
        print(f'현재 시간대: {timezone}')

        # 오늘 날짜의 로그 추가 - TB_MENU에 등록된 메뉴 사용
        print('\n=== 오늘 날짜 로그 추가 (등록된 메뉴 사용) ===')
        today_str = '2025-12-15'
        # TB_MENU에 등록된 메뉴 이름 사용
        cur.execute("INSERT INTO TB_USER_ACS_LOG (USER_ID, MENU_NM, ACS_DT) VALUES (%s, %s, %s::timestamp)", ('admin', '관리자 설정', today_str + ' 10:00:00'))
        cur.execute("INSERT INTO TB_USER_ACS_LOG (USER_ID, MENU_NM, ACS_DT) VALUES (%s, %s, %s::timestamp)", ('admin', '데이터 수집 일정', today_str + ' 10:01:00'))
        conn.commit()
        print(f'admin 사용자의 {today_str} 날짜 실제 메뉴 로그 2건 추가 완료')

        # 추가 후 다시 확인
        cur.execute("SELECT COUNT(*) FROM TB_USER_ACS_LOG WHERE ACS_DT::date = %s AND USER_ID = 'admin'", (today_str,))
        today_count_after = cur.fetchone()[0]
        print(f'{today_str} 날짜 admin 로그 건수: {today_count_after}')

        # 추가 후 다시 확인
        cur.execute("SELECT COUNT(*) FROM TB_USER_ACS_LOG WHERE ACS_DT::date = CURRENT_DATE AND USER_ID = 'admin'")
        new_today_admin_count = cur.fetchone()[0]
        print(f'테스트 로그 추가 후 오늘 admin 건수: {new_today_admin_count}')

        # 최근 로그 확인
        cur.execute("SELECT ACS_DT, USER_ID, MENU_NM FROM TB_USER_ACS_LOG WHERE USER_ID = 'admin' ORDER BY ACS_DT DESC LIMIT 2")
        latest_logs = cur.fetchall()
        print('가장 최근 admin 로그:')
        for log in latest_logs:
            print(f'{log[0]} | {log[1]} | {log[2]}')

        # 통계 쿼리 직접 테스트
        print('\n=== 통계 쿼리 테스트 ===')
        from dao.analytics_dao import AnalyticsDAO
        dao = AnalyticsDAO(conn)

        menu_stats = dao.get_menu_access_stats(view_type='daily', start_date='2025-12-15', end_date='2025-12-15')
        total_stats = dao.get_total_access_stats(view_type='daily', start_date='2025-12-15', end_date='2025-12-15')

        print(f'menu_access_stats: {menu_stats}')
        print(f'total_access_stats: {total_stats}')

except Exception as e:
    print(f'에러: {e}')
    import traceback
    traceback.print_exc()
finally:
    if 'conn' in locals():
        conn.close()
