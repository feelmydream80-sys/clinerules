import psycopg2
from my_setting.db_config import DB_CONFIG

try:
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()
    cursor.execute("SELECT column_name FROM information_schema.columns WHERE table_name = 'tb_data_clt_schd_sett' ORDER BY ordinal_position;")
    columns = cursor.fetchall()
    print("Columns in tb_data_clt_schd_sett:")
    for col in columns:
        print(f"  - {col[0]}")
    cursor.close()
    conn.close()
except Exception as e:
    print(f"Error: {e}")
