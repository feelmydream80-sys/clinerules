import psycopg2
import random
from datetime import datetime, timedelta
from msys.database import get_db_connection

# --- 설정 ---
YEARS_TO_GENERATE = [2024, 2025]
LOGS_PER_YEAR = 20
USER_IDS = ['user1', 'user2', 'user3', 'admin', 'test_user']
MENU_NAMES = [
    '대시보드', '잔디', '상세데이터', '차트분석', '데이터분석', 
    '데이터 명세서', 'API 테스트', '관리자 설정'
]
# --- 설정 끝 ---

def get_random_timestamp(year):
    """지정된 연도 내에서 무작위 날짜와 시간을 생성합니다."""
    start_date = datetime(year, 1, 1)
    end_date = datetime(year, 12, 31)
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + timedelta(days=random_number_of_days)
    random_time = timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59), seconds=random.randint(0, 59))
    return random_date + random_time

def generate_logs():
    """테스트 로그 데이터를 생성하고 데이터베이스에 삽입합니다."""
    conn = None
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        
        total_inserted = 0
        for year in YEARS_TO_GENERATE:
            print(f"--- {year}년 데이터 생성 시작 ---")
            for i in range(LOGS_PER_YEAR):
                user_id = random.choice(USER_IDS)
                menu_nm = random.choice(MENU_NAMES)
                acs_dt = get_random_timestamp(year)
                
                try:
                    cur.execute(
                        "INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES (%s, %s, %s)",
                        (user_id, menu_nm, acs_dt)
                    )
                    print(f"  - 입력 성공: {user_id}, {menu_nm}, {acs_dt.strftime('%Y-%m-%d %H:%M:%S')}")
                    total_inserted += 1
                except Exception as e:
                    print(f"  - 입력 실패: {user_id}, {menu_nm}, {acs_dt.strftime('%Y-%m-%d %H:%M:%S')} - {e}")

            print(f"--- {year}년 데이터 생성 완료 ---")

        conn.commit()
        print(f"\n총 {total_inserted}개의 테스트 로그를 성공적으로 삽입했습니다.")

    except Exception as e:
        print(f"데이터 생성 중 오류 발생: {e}")
    finally:
        if conn:
            conn.close()
            print("데이터베이스 연결을 닫았습니다.")

if __name__ == "__main__":
    print("테스트 데이터 생성을 시작합니다.")
    generate_logs()
