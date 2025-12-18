import psycopg2
from my_setting.db_config import DB_CONFIG
from dotenv import load_dotenv
import os

load_dotenv()

def execute_sql_file(file_path):
    """Executes a SQL file using the database connection."""
    try:
        db_config_with_encoding = DB_CONFIG.copy()
        db_config_with_encoding['client_encoding'] = 'UTF8'
        with psycopg2.connect(**db_config_with_encoding) as conn:
            with conn.cursor() as cur:
                with open(file_path, 'r', encoding='utf-8') as f:
                    sql = f.read()
                    cur.execute(sql)
                print(f"Successfully executed SQL script: {file_path}")
    except Exception as e:
        print(f"Error executing SQL script {file_path}: {e}")

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        execute_sql_file(sys.argv[1])
    else:
        print("Usage: python execute_sql.py <path_to_sql_file>")
