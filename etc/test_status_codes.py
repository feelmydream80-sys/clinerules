from msys_app import create_app
from msys.database import get_db_connection
from service.status_code_service import get_status_codes

app = create_app()
with app.app_context():
    with get_db_connection() as conn:
        try:
            codes = get_status_codes()
            print("Status codes loaded successfully:", codes)
        except Exception as e:
            print("Error loading status codes:", e)