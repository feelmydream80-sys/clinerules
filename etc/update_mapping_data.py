import logging
from mapper.mapping_mapper import MappingMapper
from msys.database import get_db_connection

# 로깅 설정
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# 추가/수정할 매핑 데이터 정의
# bf_col_nm: 프론트엔드(레거시)에서 사용하는 키
# new_col_nm: DB(tb_mngr_sett)의 컬럼명
MAPPING_DATA_TO_ADD = [
    # --- 기존 데이터 ---
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CD', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cd', 'expl': 'Legacy CD to new cd'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CNN_FAILR_THRS_VAL', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cnn_failr_thrs_val', 'expl': 'Connection failure threshold'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CNN_WARN_THRS_VAL', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cnn_warn_thrs_val', 'expl': 'Connection warning threshold'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CNN_FAILR_ICON_ID', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cnn_failr_icon_id', 'expl': 'Icon ID for connection failure'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CNN_FAILR_WRD_COLR', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cnn_failr_wrd_colr', 'expl': 'Word color for connection failure'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CNN_WARN_ICON_ID', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cnn_warn_icon_id', 'expl': 'Icon ID for connection warning'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CNN_WARN_WRD_COLR', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cnn_warn_wrd_colr', 'expl': 'Word color for connection warning'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CNN_SUCS_ICON_ID', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cnn_sucs_icon_id', 'expl': 'Icon ID for connection success'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CNN_SUCS_WRD_COLR', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cnn_sucs_wrd_colr', 'expl': 'Word color for connection success'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'DLY_SUCS_RT_THRS_VAL', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'dly_sucs_rt_thrs_val', 'expl': 'Daily success rate threshold'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'DD7_SUCS_RT_THRS_VAL', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'dd7_sucs_rt_thrs_val', 'expl': '7-day success rate threshold'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'MTHL_SUCS_RT_THRS_VAL', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'mthl_sucs_rt_thrs_val', 'expl': 'Monthly success rate threshold'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'MC6_SUCS_RT_THRS_VAL', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'mc6_sucs_rt_thrs_val', 'expl': '6-month success rate threshold'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'YY1_SUCS_RT_THRS_VAL', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'yy1_sucs_rt_thrs_val', 'expl': '1-year success rate threshold'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'SUCS_RT_SUCS_ICON_ID', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'sucs_rt_sucs_icon_id', 'expl': 'Icon ID for success rate success'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'SUCS_RT_SUCS_WRD_COLR', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'sucs_rt_sucs_wrd_colr', 'expl': 'Word color for success rate success'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'SUCS_RT_WARN_ICON_ID', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'sucs_rt_warn_icon_id', 'expl': 'Icon ID for success rate warning'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'SUCS_RT_WARN_WRD_COLR', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'sucs_rt_warn_wrd_colr', 'expl': 'Word color for success rate warning'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CHRT_COLR', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'chrt_colr', 'expl': 'Chart color'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CHRT_DSP_YN', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'chrt_dsp_yn', 'expl': 'Chart display Y/N'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'GRASS_CHRT_MIN_COLR', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'grass_chrt_min_colr', 'expl': 'Grass chart min color'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'GRASS_CHRT_MAX_COLR', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'grass_chrt_max_colr', 'expl': 'Grass chart max color'},
    
    # --- 누락된 매핑 데이터 추가 ---
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CD_NM', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cd_nm', 'expl': 'Legacy CD_NM to new cd_nm'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'CD_DESC', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'cd_desc', 'expl': 'Legacy CD_DESC to new cd_desc'},
    {'bf_tbl_nm': 'TB_MNGR_SETT', 'bf_col_nm': 'ITEM5', 'new_tbl_nm': 'TB_MNGR_SETT', 'new_col_nm': 'item5', 'expl': 'Legacy ITEM5 to new item5'},
]

def upsert_mapping_data(cursor, mapping_list):
    """
    주어진 매핑 데이터 리스트를 기반으로 TB_COL_MAPP 테이블에 데이터를 추가하거나 업데이트합니다.
    """
    added_count = 0
    updated_count = 0

    for item in mapping_list:
        # bf_col_nm과 new_tbl_nm을 기준으로 기존 데이터 확인
        cursor.execute(
            "SELECT mapp_id FROM TB_COL_MAPP WHERE bf_col_nm = %s AND new_tbl_nm = %s",
            (item['bf_col_nm'], item['new_tbl_nm'])
        )
        result = cursor.fetchone()

        if result:
            # 데이터가 존재하면 업데이트
            mapp_id = result[0]
            update_query = """
                UPDATE TB_COL_MAPP SET 
                    bf_tbl_nm = %(bf_tbl_nm)s, 
                    new_col_nm = %(new_col_nm)s, 
                    expl = %(expl)s,
                    upd_dt = CURRENT_TIMESTAMP
                WHERE mapp_id = %(mapp_id)s
            """
            cursor.execute(update_query, {**item, 'mapp_id': mapp_id})
            updated_count += 1
        else:
            # 데이터가 없으면 새로 추가
            insert_query = """
                INSERT INTO TB_COL_MAPP (bf_tbl_nm, bf_col_nm, new_tbl_nm, new_col_nm, expl)
                VALUES (%(bf_tbl_nm)s, %(bf_col_nm)s, %(new_tbl_nm)s, %(new_col_nm)s, %(expl)s)
            """
            cursor.execute(insert_query, item)
            added_count += 1
            
    return added_count, updated_count

def get_icon_mapping_data():
    """
    TB_ICON 테이블의 컬럼 정보를 동적으로 읽어와 매핑 데이터를 생성합니다.
    """
    logging.info("TB_ICON 테이블의 스키마 정보를 읽어옵니다...")
    mapping_mapper = MappingMapper()
    columns = mapping_mapper.get_all_schema_columns()
    
    icon_columns = [col['column_name'] for col in columns if col['table_name'] == 'TB_ICON_MST']
    
    icon_mapping_data = []
    for col in icon_columns:
        icon_mapping_data.append({
            'bf_tbl_nm': 'TB_ICON_MST',
            'bf_col_nm': col.upper(),
            'new_tbl_nm': 'TB_ICON_MST',
            'new_col_nm': col.lower(),
            'expl': f'Legacy {col.upper()} to new {col.lower()}'
        })
    
    logging.info(f"TB_ICON_MST 테이블에 대한 {len(icon_mapping_data)}개의 매핑 데이터를 생성했습니다.")
    return icon_mapping_data

def main():
    """
    TB_COL_MAPP 테이블의 매핑 데이터를 전체적으로 업데이트합니다.
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # 1. TB_MNGR_SETT 데이터 업데이트
        logging.info("--- TB_MNGR_SETT 매핑 데이터 업데이트 시작 ---")
        added_sett, updated_sett = upsert_mapping_data(cursor, MAPPING_DATA_TO_ADD)
        logging.info(f"TB_MNGR_SETT 업데이트 완료. 추가: {added_sett}, 수정: {updated_sett}")

        # 2. TB_ICON 데이터 업데이트
        logging.info("--- TB_ICON 매핑 데이터 업데이트 시작 ---")
        icon_mapping_data = get_icon_mapping_data()
        added_icon, updated_icon = upsert_mapping_data(cursor, icon_mapping_data)
        logging.info(f"TB_ICON 업데이트 완료. 추가: {added_icon}, 수정: {updated_icon}")

        conn.commit()
        logging.info("✅ 모든 매핑 데이터 업데이트가 성공적으로 완료되었습니다.")

    except Exception as e:
        if conn:
            conn.rollback()
        logging.error(f"❌ 매핑 데이터 업데이트 중 오류 발생: {e}", exc_info=True)
    finally:
        if conn:
            conn.close()
            logging.info("데이터베이스 연결이 종료되었습니다.")

if __name__ == "__main__":
    main()
