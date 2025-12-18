from dao.sql_loader import load_sql

class UserSQL:
    @staticmethod
    def find_by_id():
        return load_sql('user/find_by_id.sql')

    @staticmethod
    def find_all():
        return load_sql('user/find_all.sql')

    @staticmethod
    def delete_by_id():
        return load_sql('user/delete_by_id.sql')

    @staticmethod
    def save():
        return load_sql('user/save.sql')

    @staticmethod
    def update_status():
        return load_sql('user/update_status.sql')

    @staticmethod
    def update_password():
        return load_sql('user/update_password.sql')

    @staticmethod
    def find_user_permissions():
        return load_sql('user/find_user_permissions.sql')

    @staticmethod
    def find_all_permissions():
        return load_sql('user/find_all_permissions.sql')

    @staticmethod
    def find_all_menus():
        return load_sql('user/find_all_menus.sql')

    @staticmethod
    def delete_user_permissions():
        return load_sql('user/delete_user_permissions.sql')

    @staticmethod
    def insert_user_permission():
        return load_sql('user/insert_user_permission.sql')

    @staticmethod
    def find_user_menus_sorted():
        return load_sql('user/find_user_menus_sorted.sql')
