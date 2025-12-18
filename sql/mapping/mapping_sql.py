from dao.sql_loader import load_sql

class MappingSQL:
    @staticmethod
    def add_mapping():
        return load_sql('mapping/add_mapping.sql')

    @staticmethod
    def delete_mapping():
        return load_sql('mapping/delete_mapping.sql')

    @staticmethod
    def get_all_mappings():
        return load_sql('mapping/get_all_mappings.sql')

    @staticmethod
    def get_all_schema_columns():
        return load_sql('mapping/get_all_schema_columns.sql')

    @staticmethod
    def update_mapping():
        return load_sql('mapping/update_mapping.sql')
