from msys_app import create_app
from msys.database import get_db_connection
from dao.con_mst_dao import ConMstDAO

app = create_app()
with app.app_context():
    with get_db_connection() as conn:
        dao = ConMstDAO(conn)
        result = dao.get_error_code_map()
        print("CD900 error codes:", result)
