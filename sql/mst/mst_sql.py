from dao.sql_loader import load_sql

class MstSQL:
    @staticmethod
    def get_all_mst():
        return load_sql('mst/get_all_mst.sql')

    @staticmethod
    def get_error_code_map():
        return load_sql('mst/get_error_code_map.sql')

    @staticmethod
    def get_mst_by_cd():
        return load_sql('mst/get_mst_by_cd.sql')
