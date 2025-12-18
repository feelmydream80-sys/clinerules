import os
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

# 관리자로 지정할 사용자 ID
ADMIN_USER_ID = 'admin'
ADMIN_PERMISSION = 'mngr_sett'

def reset_admin_permission():
    """
    모든 사용자의 권한을 초기화하고 지정된 관리자에게만 관리 권한을 부여합니다.
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cursor = conn.cursor()

        # 1. TB_USER_AUTH_CTRL 테이블의 모든 데이터 삭제
        print("모든 사용자의 기존 권한을 삭제합니다...")
        cursor.execute("DELETE FROM TB_USER_AUTH_CTRL")
        print("모든 권한 삭제 완료.")

        # 2. 지정된 관리자에게 'mngr_sett' 권한 부여
        print(f"'{ADMIN_USER_ID}' 사용자에게 관리자 권한('{ADMIN_PERMISSION}')을 부여합니다...")
        cursor.execute(
            "INSERT INTO TB_USER_AUTH_CTRL (USER_ID, MENU_ID) VALUES (%s, %s)",
            (ADMIN_USER_ID, ADMIN_PERMISSION)
        )
        print(f"'{ADMIN_USER_ID}' 사용자에게 관리자 권한 부여 완료.")

        # 변경사항 커밋
        conn.commit()
        print("권한 재설정 작업이 성공적으로 완료되었습니다.")

    except Exception as e:
        if 'conn' in locals() and conn:
            conn.rollback() # 오류 발생 시 롤백
        print(f"권한 재설정 중 오류 발생: {e}")
    finally:
        if 'conn' in locals() and conn:
            cursor.close()
            conn.close()
            print("데이터베이스 연결 종료.")

if __name__ == '__main__':
    reset_admin_permission()
