# dao/user_dao.py
from typing import List, Dict, Any
from psycopg2.extras import RealDictCursor
from dao.sql_loader import load_sql
from msys.column_mapper import convert_to_legacy_columns

class UserDao:
    def __init__(self, conn):
        self.conn = conn

    def find_by_id(self, user_id: str) -> Dict[str, Any]:
        """ID로 사용자를 찾습니다."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(load_sql('user/find_by_id.sql'), (user_id,))
            data = cursor.fetchone()
            return convert_to_legacy_columns('TB_USER', data)

    def find_all(self) -> List[Dict[str, Any]]:
        """모든 사용자를 찾고, 각 사용자가 'admin' 메뉴 권한을 가졌는지 확인합니다."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            query = """
                SELECT 
                    u.USER_ID, 
                    u.ACC_STS, 
                    u.ACC_CRE_DT,
                    EXISTS (
                        SELECT 1 
                        FROM TB_USER_AUTH_CTRL a 
                        WHERE a.USER_ID = u.USER_ID AND a.MENU_ID = 'mngr_sett'
                    ) as is_admin
                FROM TB_USER u 
                ORDER BY u.ACC_CRE_DT DESC
            """
            cursor.execute(query)
            data = cursor.fetchall()
            return convert_to_legacy_columns('TB_USER', data)

    def delete_by_id(self, user_id: str) -> None:
        """ID로 사용자를 삭제합니다."""
        with self.conn.cursor() as cursor:
            # 관련된 접근 제어 데이터도 함께 삭제합니다 (ON DELETE CASCADE가 설정되어 있지 않은 경우).
            cursor.execute(load_sql('user/delete_user_permissions.sql'), (user_id,))
            cursor.execute(load_sql('user/delete_by_id.sql'), (user_id,))

    def save(self, user_id: str, hashed_password: str) -> None:
        """새로운 사용자를 저장합니다."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                load_sql('user/save.sql'),
                (user_id, hashed_password, 'PENDING')
            )

    def update_status(self, user_id: str, status: str) -> None:
        """사용자 상태를 업데이트합니다."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                "UPDATE TB_USER SET ACC_STS = %s, ACC_APR_DT = CASE WHEN %s = 'APPROVED' THEN CURRENT_TIMESTAMP ELSE ACC_APR_DT END WHERE USER_ID = %s",
                (status, status, user_id)
            )

    def update_password(self, user_id: str, hashed_password: str) -> None:
        """사용자 비밀번호를 업데이트합니다."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                load_sql('user/update_password.sql'),
                (hashed_password, user_id)
            )

    def find_user_permissions(self, user_id: str) -> List[str]:
        """사용자의 모든 메뉴 접근 권한을 조회합니다."""
        with self.conn.cursor() as cursor:
            cursor.execute(
                load_sql('user/find_user_permissions.sql'),
                (user_id,)
            )
            return [row[0] for row in cursor.fetchall()]

    def find_all_menus(self) -> List[Dict[str, Any]]:
        """모든 메뉴 목록을 조회합니다."""
        with self.conn.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(load_sql('user/find_all_menus.sql'))
            data = cursor.fetchall()
            return convert_to_legacy_columns('TB_MENU', data)

    def update_user_permissions(self, user_id: str, menu_ids: List[str]) -> None:
        """사용자의 메뉴 접근 권한을 업데이트합니다."""
        with self.conn.cursor() as cursor:
            # 먼저 해당 사용자의 모든 권한을 삭제합니다.
            cursor.execute("DELETE FROM TB_USER_AUTH_CTRL WHERE USER_ID = %s", (user_id,))
            # 새로운 권한을 추가합니다.
            if menu_ids:
                # mogrify를 사용하여 SQL 인젝션 방지
                values = [(user_id, menu_id) for menu_id in menu_ids]
                args_str = ','.join(cursor.mogrify("(%s,%s)", v).decode('utf-8') for v in values)
                cursor.execute("INSERT INTO TB_USER_AUTH_CTRL (USER_ID, MENU_ID) VALUES " + args_str)
