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
            # 시간대 확인
            cur.execute('SHOW timezone')
            current_tz = cur.fetchone()[0]
            print(f'현재 DB 시간대: {current_tz}')

            # 현재 날짜/시간 확인
            cur.execute('SELECT CURRENT_DATE, CURRENT_TIMESTAMP')
            current_info = cur.fetchone()
            print(f'DB 현재 날짜: {current_info[0]}')
            print(f'DB 현재 시간: {current_info[1]}')

            # 시스템 시간과 비교
            import datetime
            now = datetime.datetime.now()
            print(f'시스템 현재 시간: {now}')
            print(f'시스템 날짜: {now.date()}')

            # 날짜 차이 계산
            db_date = current_info[0]
            sys_date = now.date()
            diff = (sys_date - db_date).days
            print(f'날짜 차이: {diff}일 (시스템 - DB)')

except Exception as e:
    print(f'에러: {e}')
finally:
    if 'conn' in locals():
        conn.close()
