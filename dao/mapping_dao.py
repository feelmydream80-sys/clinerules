from psycopg2.extras import RealDictCursor
from dao.sql_loader import load_sql

class MappingDAO:
    def __init__(self, db_connection):
        self.conn = db_connection

    def get_all_mappings(self):
        """모든 컬럼 매핑 정보를 데이터베이스에서 조회합니다."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(load_sql('mapping/get_all_mappings.sql'))
            mappings = cur.fetchall()
            return mappings

    def add_mapping(self, mapping_data):
        """새로운 매핑 정보를 데이터베이스에 추가합니다."""
        with self.conn.cursor() as cur:
            cur.execute(load_sql('mapping/add_mapping.sql'), mapping_data)

    def update_mapping(self, mapping_data):
        """기존 매핑 정보를 수정합니다."""
        with self.conn.cursor() as cur:
            cur.execute(load_sql('mapping/update_mapping.sql'), mapping_data)

    def delete_mapping(self, mapp_id):
        """매핑 정보를 삭제합니다."""
        with self.conn.cursor() as cur:
            cur.execute(load_sql('mapping/delete_mapping.sql'), (mapp_id,))

    def get_all_schema_columns(self):
        """information_schema에서 모든 테이블과 컬럼 정보를 조회합니다."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(load_sql('mapping/get_all_schema_columns.sql'))
            columns = cur.fetchall()
            return columns
