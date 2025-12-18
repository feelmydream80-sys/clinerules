#!/usr/bin/env python3
"""
Test script for schedule_settings API debugging
"""
import sys
import os
sys.path.append('.')

from flask import Flask
from msys.database import get_db_connection, init_db_pool
from service.mngr_sett_service import MngrSettService

def test_schedule_settings():
    """Test the schedule settings API end-to-end"""
    app = Flask(__name__)

    with app.app_context():
        try:
            print("=== Testing Schedule Settings API ===")

            # Initialize DB pool
            init_db_pool()
            print("DB pool initialized")

            # Get database connection
            conn = get_db_connection()
            print("Database connection established")

            # Create service
            service = MngrSettService(conn)
            print("MngrSettService created")

            # Call the service method
            settings = service.get_schedule_settings_service()
            print("Service method called successfully")

            if settings:
                print(f"Settings returned: {type(settings)}")
                print(f"Keys: {list(settings.keys()) if isinstance(settings, dict) else 'Not a dict'}")

                # Try to jsonify the result
                from flask import jsonify
                json_result = jsonify(settings)
                print("JSON conversion successful")
                json_data = json_result.get_json()
                print(f"JSON data keys: {list(json_data.keys())}")
                print("Sample values:")
                for k, v in list(json_data.items())[:5]:
                    print(f"  {k}: {v} ({type(v).__name__})")
            else:
                print("No settings returned from service")

            conn.close()
            print("Database connection closed")

        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_schedule_settings()
