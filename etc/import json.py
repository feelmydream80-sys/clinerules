import json
import logging
from msys.database import get_db_connection

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# JSON 파일의 키를 DB 테이블 컬럼명으로 매핑
KEY_MAPPING = {
    "cd": "cd",
    "cf_fail_cnt": "cnn_failr_thrs_val",
    "cf_warning_cnt": "cnn_warn_thrs_val",
    "cf_fail_icon": "cnn_failr_icon_id",
    "cf_fail_wd_color": "cnn_failr_wrd_colr",
    "cf_warning_icon": "cnn_warn_icon_id",
    "cf_warning_wd_color": "cnn_warn_wrd_colr",
    "cf_success_icon": "cnn_sucs_icon_id",
    "cf_success_wd_color": "cnn_sucs_wrd_colr",
    "sr_day_th": "dly_sucs_rt_thrs_val",
    "sr_week_th": "dd7_sucs_rt_thrs_val",
    "sr_month_th": "mthl_sucs_rt_thrs_val",
    "sr_half_th": "mc6_sucs_rt_thrs_val",
    "sr_year_th": "yy1_sucs_rt_thrs_val",
    "sr_success_icon": "sucs_rt_sucs_icon_id",
    "sr_success_wd_color": "sucs_rt_sucs_wrd_colr",
    "sr_warning_icon": "sucs_rt_warn_icon_id",
    "sr_warning_wd_color": "sucs_rt_warn_wrd_colr",
    "chart_color": "chrt_colr",
    "display_yn": "chrt_dsp_yn",
    "jandi_color_min": "grass_chrt_min_colr",
    "jandi_color_max": "grass_chrt_max_colr"
}

def restore_settings():
    """
    JSON 파일에서 설정을 읽어와 DB에 복원합니다.
    """
    json_file_path = 'c:/Users/Administrator/Downloads/admin_settings (4).json'
    
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            settings_data = json.load(f)
        logging.info(f"✅ Successfully loaded {len(settings_data)} records from {json_file_path}")
    except FileNotFoundError:
        logging.error(f"❌ File not found: {json_file_path}")
        return
    except json.JSONDecodeError:
        logging.error(f"❌ Failed to decode JSON from {json_file_path}")
        return

    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        restored_count = 0
        for item in settings_data:
            # 데이터를 DB 컬럼에 맞게 변환
            new_item = {KEY_MAPPING[k]: v for k, v in item.items() if k in KEY_MAPPING}
            
            # SQL 쿼리 생성
            columns = ", ".join(new_item.keys())
            placeholders = ", ".join(["%s"] * len(new_item))
            
            update_assignments = ", ".join([f"{col} = EXCLUDED.{col}" for col in new_item.keys() if col != 'cd'])
            
            sql = f"""
                INSERT INTO tb_mngr_sett ({columns})
                VALUES ({placeholders})
                ON CONFLICT (cd) DO UPDATE SET {update_assignments};
            """
            
            try:
                cursor.execute(sql, list(new_item.values()))
                restored_count += 1
            except Exception as e:
                logging.error(f"❌ Failed to insert/update record for cd='{new_item.get('cd')}': {e}")

        conn.commit()
        logging.info(f"✅ Successfully restored {restored_count} records into tb_mngr_sett.")

    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"❌ An error occurred during the database operation: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()
            logging.info("Database connection closed.")

if __name__ == "__main__":
    restore_settings()
