import csv
from msys.database import get_db_connection
from mapper.mapping_mapper import MappingMapper
from prettytable import PrettyTable

def get_mappings_from_db():
    """데이터베이스에서 매핑 데이터를 가져옵니다."""
    try:
        conn = get_db_connection()
        mapper = MappingMapper(conn)
        return mapper.get_all_mappings()
    finally:
        if conn:
            conn.close()

def main():
    """메인 실행 함수"""
    db_mappings_list = get_mappings_from_db()

    if not db_mappings_list:
        print("No data found in 'tb_col_mapp'.")
        return

    print(f"--- All Data in tb_col_mapp ({len(db_mappings_list)} rows) ---")
    
    table = PrettyTable()
    # 헤더를 DB에서 가져온 데이터의 키로 설정
    table.field_names = db_mappings_list[0].keys()
    table.align = "l"

    for row in db_mappings_list:
        table.add_row(row.values())
        
    print(table)

if __name__ == "__main__":
    try:
        import prettytable
    except ImportError:
        print("prettytable is not installed. Please install it using: pip install prettytable")
    else:
        main()
