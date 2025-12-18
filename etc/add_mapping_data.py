import csv
from msys.database import get_db_connection
from dao.mapping_dao import MappingDAO

def add_admin_settings_mapping():
    """column_mapping.csv 파일을 읽어 TB_COL_MAPP 테이블에 데이터를 추가합니다."""
    try:
        conn = get_db_connection()
        mapping_dao = MappingDAO(conn)
        
        with open('column_mapping.csv', 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            next(reader)  # Skip header
            next(reader)  # Skip second header

            for row in reader:
                # CSV 파일의 각 행을 데이터베이스에 맞게 매핑
                mapping_data = {
                    'bf_tbl_nm': row[0],
                    'new_tbl_nm': row[1],
                    'bf_col_nm': row[2],
                    'expl': row[3],
                    'new_col_nm': row[4]
                }
                mapping_dao.add_mapping(mapping_data)
        
        conn.commit()
        print("Data from 'column_mapping.csv' has been added to 'tb_col_mapp'.")

    except Exception as e:
        if conn:
            conn.rollback()
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    add_admin_settings_mapping()
