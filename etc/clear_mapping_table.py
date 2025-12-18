from msys.database import get_db_connection

def clear_table():
    """tb_col_mapp 테이블의 모든 데이터를 삭제합니다."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cur:
            cur.execute("DELETE FROM tb_col_mapp")
            conn.commit()
            print("Table 'tb_col_mapp' has been cleared.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    clear_table()
