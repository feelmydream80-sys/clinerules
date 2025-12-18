import os
import csv
import psycopg2
from dotenv import load_dotenv

# .env 파일에서 환경 변수 로드
load_dotenv()

# 데이터베이스 연결 정보
DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "port": os.getenv("DB_PORT")
}

# 백업할 테이블 목록
TABLES_TO_BACKUP = [
    'TB_USER',
    'TB_MENU',
    'TB_USER_AUTH_CTRL'
]

def backup_data():
    """
    지정된 테이블의 데이터를 CSV 파일로 백업합니다.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        for table_name in TABLES_TO_BACKUP:
            backup_filename = f'backup_{table_name}.csv'
            
            print(f"'{table_name}' 테이블 데이터 백업 시작 -> {backup_filename}")

            # 테이블 데이터 조회
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            
            # 컬럼명 조회
            column_names = [desc[0] for desc in cursor.description]

            # CSV 파일로 저장
            with open(backup_filename, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                # 헤더 작성
                writer.writerow(column_names)
                # 데이터 작성
                writer.writerows(rows)
            
            print(f"'{table_name}' 테이블 데이터 백업 완료.")

    except Exception as e:
        print(f"백업 중 오류 발생: {e}")
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()
            print("데이터베이스 연결 종료.")

if __name__ == '__main__':
    backup_data()
