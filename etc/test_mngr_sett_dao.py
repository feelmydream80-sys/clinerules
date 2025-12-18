# test_mngr_sett_dao.py (v5 - Final)
"""
수정된 ScheduleSettingsDAO의 get/update 기능을 최종 검증합니다.
"""
import os
import sys
import psycopg2
from dotenv import load_dotenv

# --- 설정 ---
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

env_path = os.path.join(project_root, '.env')
if not os.path.exists(env_path):
    print(f"❌ 치명적 오류: '{env_path}' 파일을 찾을 수 없습니다.")
    sys.exit(1)

load_dotenv(dotenv_path=env_path)
print(f"✅ .env 파일 로드 시도: '{env_path}'")

# --- 테스트 대상 임포트 ---
from my_setting.db_config import DB_CONFIG
from dao.schedule_settings_dao import ScheduleSettingsDAO

def get_standalone_db_connection():
    print("\n--- DB 연결 인자 검증 ---")
    is_config_valid = True
    for key, value in DB_CONFIG.items():
        if value is None:
            print(f"  - ❌ '{key}': 값 없음 (None)")
            is_config_valid = False
        else:
            masked_value = '****' + value[-2:] if key == 'password' and len(value) > 4 else value
            print(f"  - ✅ '{key}': {masked_value}")
    if not is_config_valid: return None
    try:
        print("\n데이터베이스에 연결을 시도합니다...")
        conn = psycopg2.connect(**DB_CONFIG)
        print("🎉 데이터베이스 연결 성공!")
        return conn
    except Exception as e:
        print(f"\n❌ 데이터베이스 연결 오류: {e}")
        return None

def main():
    print("🚀 ScheduleSettingsDAO CRUD 기능 최종 테스트를 시작합니다.")
    conn = None
    original_settings = None
    try:
        conn = get_standalone_db_connection()
        if conn is None: return

        dao = ScheduleSettingsDAO(conn)
        
        # 1. 초기 데이터 조회 및 백업
        print("\n--- 1. 초기 데이터 조회 ---")
        original_settings = dao.get_schedule_settings()
        if not original_settings:
            print("❌ 테스트 실패: 초기 데이터를 조회할 수 없습니다.")
            return
        print(f"✅ 초기 데이터: {original_settings}")

        # 2. 데이터 업데이트 테스트
        print("\n--- 2. 데이터 업데이트 테스트 ---")
        test_data = original_settings.copy()
        # 실제 테이블에 존재하는 컬럼으로 테스트 값 변경
        test_data['grp_min_cnt'] = 99
        test_data['prgs_rt_red_thrsval'] = 15
        test_data['updr_id'] = 'test_runner'
        
        print(f"🔄 업데이트할 데이터: grp_min_cnt=99, prgs_rt_red_thrsval=15")
        dao.update_schedule_settings(test_data)
        conn.commit()
        print("✅ 업데이트 쿼리 실행 완료.")

        # 3. 업데이트 결과 검증
        print("\n--- 3. 업데이트 결과 검증 ---")
        updated_settings = dao.get_schedule_settings()
        print(f"✅ 업데이트 후 데이터: {updated_settings}")
        
        if updated_settings.get('grp_min_cnt') == 99 and updated_settings.get('prgs_rt_red_thrsval') == 15:
            print("🎉 검증 성공: 데이터가 성공적으로 업데이트되었습니다.")
        else:
            print("❌ 검증 실패: 데이터가 올바르게 업데이트되지 않았습니다.")

    except Exception as e:
        print(f"❌ DAO 테스트 중 예기치 않은 오류 발생: {e}")
        if conn: conn.rollback()
    finally:
        # 4. 데이터 원상 복구
        if conn and original_settings:
            print("\n--- 4. 데이터 원상 복구 ---")
            try:
                # 복구 시에도 updr_id를 설정해주는 것이 좋음
                original_settings['updr_id'] = 'test_reverter'
                dao.update_schedule_settings(original_settings)
                conn.commit()
                print("✅ 데이터를 초기 상태로 복구했습니다.")
            except Exception as e:
                print(f"❌ 데이터 복구 중 오류 발생: {e}")
                
        if conn:
            conn.close()
            print("\n✅ 데이터베이스 연결을 종료했습니다.")
        print("🏁 테스트를 종료합니다.")

if __name__ == "__main__":
    main()