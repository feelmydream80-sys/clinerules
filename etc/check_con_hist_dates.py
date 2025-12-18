# -*- coding: utf-8 -*-
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from msys.database import get_db_connection
from msys_app import create_app

def list_all_tables():
    """
    현재 데이터베이스의 모든 테이블 목록을 조회하여 출력합니다.
    """
    app = create_app()
    with app.app_context():
        conn = None
        try:
            conn = get_db_connection()
            with conn.cursor() as cur:
                print("현재 데이터베이스의 모든 테이블 목록을 조회합니다...")
                
                cur.execute("""
                    SELECT tablename 
                    FROM pg_catalog.pg_tables 
                    WHERE schemaname != 'pg_catalog' AND schemaname != 'information_schema';
                """)
                
                tables = cur.fetchall()

                if not tables:
                    print("\n[결론] 테이블이 존재하지 않습니다.")
                else:
                    print("\n[테이블 목록]")
                    for table in tables:
                        print(f"- {table[0]}")

        except Exception as e:
            print(f"오류: 데이터베이스 확인 중 오류가 발생했습니다: {e}")
        finally:
            if conn:
                conn.close()
                print("DB 연결을 닫았습니다.")

if __name__ == '__main__':
    list_all_tables()
