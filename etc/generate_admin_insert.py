# generate_admin_insert.py
from service.password_service import PasswordService

def generate_admin_sql():
    """
    'admin' 사용자를 'APPROVED' 상태로 데이터베이스에 삽입하는 SQL 문을 생성합니다.
    비밀번호는 'admin'으로 설정됩니다.
    """
    password_service = PasswordService()
    user_id = 'admin'
    password = 'admin'

    # 애플리케이션의 해싱 로직을 그대로 사용
    hashed_password = password_service.hash_password(password).decode('utf-8')

    # tb_users에 사용자 정보 삽입
    sql_user = f"INSERT INTO tb_users (user_id, password, status, approved_at) VALUES ('{user_id}', '{hashed_password}', 'APPROVED', CURRENT_TIMESTAMP);"

    # [수정] Cline의 실수: menu_id는 하이픈(-)이 아닌 언더스코어(_)를 사용해야 함.
    # 앞으로 생성되는 모든 admin 계정은 언더스코어 규칙을 따르도록 수정.
    menus = ['dashboard', 'jandi', 'raw_data', 'chart_analysis', 'data_analysis', 'data_spec', 'api_test', 'admin']
    sql_permissions = "INSERT INTO tb_user_access_control (user_id, menu_id, permission) VALUES\n"
    sql_permissions += ',\n'.join([f"('{user_id}', '{menu_id}', TRUE)" for menu_id in menus])
    sql_permissions += ";"

    print("-- 아래 SQL 문을 복사하여 데이터베이스에서 실행하세요.")
    print("-- 1. 기존 admin 데이터 삭제 (오류 방지)")
    print(f"DELETE FROM tb_user_access_control WHERE user_id = '{user_id}';")
    print(f"DELETE FROM tb_users WHERE user_id = '{user_id}';")
    print("\n-- 2. 새로운 admin 데이터 삽입")
    print(sql_user)
    print(sql_permissions)

if __name__ == '__main__':
    generate_admin_sql()
