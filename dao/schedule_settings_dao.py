# dao/schedule_settings_dao.py
import logging
from typing import Dict, Optional

class ScheduleSettingsDAO:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.logger = logging.getLogger(self.__class__.__name__)

    def _execute_query(self, query: str, params: tuple = (), fetch_one: bool = False):
        self.logger.debug(f"DAO: _execute_query 호출. fetch_one={fetch_one}, params 개수={len(params)}")

        try:
            with self.conn.cursor() as cursor:
                self.logger.debug("DAO: 커서 생성 성공")

                # 쿼리 실행
                cursor.execute(query, params)
                self.logger.debug("DAO: 쿼리 실행 성공")

                if fetch_one:
                    self.logger.debug("DAO: fetch_one 모드로 단일 행 조회")
                    row = cursor.fetchone()

                    if row:
                        columns = [desc[0] for desc in cursor.description]
                        result = dict(zip(columns, row))
                        self.logger.debug(f"DAO: 단일 행 조회 성공. 컬럼 수: {len(columns)}")
                        return result
                    else:
                        self.logger.debug("DAO: 단일 행 조회 결과 없음")
                        return None

                else:
                    self.logger.debug("DAO: fetchall 모드로 다중 행 조회")
                    rows = cursor.fetchall()

                    if not rows:
                        self.logger.debug("DAO: 다중 행 조회 결과 없음")
                        return []

                    columns = [desc[0] for desc in cursor.description]
                    results = [dict(zip(columns, row)) for row in rows]
                    self.logger.debug(f"DAO: 다중 행 조회 성공. 행 수: {len(results)}, 컬럼 수: {len(columns)}")
                    return results

        except Exception as e:
            self.logger.error(f"DAO: _execute_query 실행 중 오류: {e}", exc_info=True)
            raise

    def get_schedule_settings(self) -> Optional[Dict]:
        """
        Fetches the latest schedule display settings from the database.
        The SQL now joins with the icon table to get the icon codes directly.
        """
        self.logger.info("=== DAO: get_schedule_settings() 시작 ===")
        try:
            # SQL 파일 존재 여부 확인
            #sql_file_path = 'sql/mngr_sett/get_schedule_settings.sql'
            #self.logger.info(f"DAO: SQL 파일 경로 확인: {sql_file_path}")

            #with open(sql_file_path, 'r', encoding='utf-8') as f:
             #   query = f.read()


            from dao.sql_loader import load_sql
            query = load_sql('mngr_sett/get_schedule_settings.sql')
            self.logger.info(f"DAO: SQL 파일 읽기 성공. 쿼리 길이: {len(query)}자")
            self.logger.debug(f"DAO: 실행할 SQL 쿼리:\n{query}")

            # 쿼리 실행
            self.logger.info("DAO: SQL 쿼리 실행 시작")
            settings = self._execute_query(query, fetch_one=True)
            self.logger.info(f"DAO: SQL 쿼리 실행 완료. 결과 타입: {type(settings)}")

            if settings is None:
                self.logger.warning("DAO: 쿼리 결과가 None입니다. 데이터가 없는 것 같습니다.")
                return None
            elif isinstance(settings, dict):
                self.logger.info(f"DAO: 딕셔너리 결과 반환. 키 개수: {len(settings)}")
                # 민감한 정보 제외하고 주요 키들 로깅
                safe_keys = ['sett_id', 'grp_min_cnt', 'use_yn', 'grp_brdr_styl', 'grp_colr_crtr']
                log_info = {k: v for k, v in settings.items() if k in safe_keys}
                self.logger.info(f"DAO: 주요 설정 값들: {log_info}")

                # 모든 키와 타입 로깅 (디버그 레벨)
                key_types = {k: type(v).__name__ for k, v in settings.items()}
                self.logger.debug(f"DAO: 모든 필드 타입들: {key_types}")
            else:
                self.logger.warning(f"DAO: 예상치 못한 결과 타입: {type(settings)}")

            self.logger.info("=== DAO: get_schedule_settings() 성공 완료 ===")
            return settings

        except FileNotFoundError as e:
            self.logger.error(f"DAO: SQL 파일을 찾을 수 없음: {sql_file_path}. 오류: {e}", exc_info=True)
            raise
        except UnicodeDecodeError as e:
            self.logger.error(f"DAO: SQL 파일 인코딩 오류: {e}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f"DAO: 스케줄 설정 조회 중 예외 발생: {e}", exc_info=True)
            # 추가 디버깅 정보
            try:
                import traceback
                self.logger.error(f"DAO: 스택 트레이스:\n{traceback.format_exc()}")
            except Exception:
                pass
            raise

    def update_schedule_settings(self, settings_data: Dict):
        """
        Updates an existing schedule settings record.
        """
        try:
            from dao.sql_loader import load_sql
            query = load_sql('mngr_sett/update_schedule_settings.sql')
            
            # Ensure all keys are present, providing defaults if necessary
            params = {
                'grp_min_cnt': settings_data.get('grp_min_cnt'),
                'prgs_rt_red_thrsval': settings_data.get('prgs_rt_red_thrsval'),
                'prgs_rt_org_thrsval': settings_data.get('prgs_rt_org_thrsval'),
                'succ_rt_red_thrsval': settings_data.get('succ_rt_red_thrsval'),
                'succ_rt_org_thrsval': settings_data.get('succ_rt_org_thrsval'),
                'use_yn': settings_data.get('use_yn'),
                'grp_brdr_styl': settings_data.get('grp_brdr_styl'),
                'grp_colr_crtr': settings_data.get('grp_colr_crtr'),
                'sucs_icon_id': settings_data.get('sucs_icon_id'),
                'sucs_bg_colr': settings_data.get('sucs_bg_colr'),
                'sucs_txt_colr': settings_data.get('sucs_txt_colr'),
                'fail_icon_id': settings_data.get('fail_icon_id'),
                'fail_bg_colr': settings_data.get('fail_bg_colr'),
                'fail_txt_colr': settings_data.get('fail_txt_colr'),
                'prgs_icon_id': settings_data.get('prgs_icon_id'),
                'prgs_bg_colr': settings_data.get('prgs_bg_colr'),
                'prgs_txt_colr': settings_data.get('prgs_txt_colr'),
                'nodt_icon_id': settings_data.get('nodt_icon_id'),
                'nodt_bg_colr': settings_data.get('nodt_bg_colr'),
                'nodt_txt_colr': settings_data.get('nodt_txt_colr'),
                'schd_icon_id': settings_data.get('schd_icon_id'),
                'schd_bg_colr': settings_data.get('schd_bg_colr'),
                'schd_txt_colr': settings_data.get('schd_txt_colr'),
                'updr_id': settings_data.get('updr_id'),
                'grp_prgs_icon_id': settings_data.get('grp_prgs_icon_id'),
                'grp_sucs_icon_id': settings_data.get('grp_sucs_icon_id'),
                'sett_id': settings_data.get('sett_id')
            }
            
            with self.conn.cursor() as cursor:
                cursor.execute(query, params)

        except Exception as e:
            self.logger.error(f"DAO: Failed to update schedule settings for sett_id {settings_data.get('sett_id')}: {e}", exc_info=True)
            raise

    def create_schedule_settings(self, settings_data: Dict) -> int:
        """
        Creates a new schedule settings record and returns the new sett_id.
        """
        try:
            from dao.sql_loader import load_sql
            query = load_sql('mngr_sett/create_schedule_settings.sql')

            params = {
                'grp_min_cnt': settings_data.get('grp_min_cnt'),
                'prgs_rt_red_thrsval': settings_data.get('prgs_rt_red_thrsval'),
                'prgs_rt_org_thrsval': settings_data.get('prgs_rt_org_thrsval'),
                'succ_rt_red_thrsval': settings_data.get('succ_rt_red_thrsval'),
                'succ_rt_org_thrsval': settings_data.get('succ_rt_org_thrsval'),
                'use_yn': settings_data.get('use_yn'),
                'grp_brdr_styl': settings_data.get('grp_brdr_styl'),
                'grp_colr_crtr': settings_data.get('grp_colr_crtr'),
                'sucs_icon_id': settings_data.get('sucs_icon_id'),
                'sucs_bg_colr': settings_data.get('sucs_bg_colr'),
                'sucs_txt_colr': settings_data.get('sucs_txt_colr'),
                'fail_icon_id': settings_data.get('fail_icon_id'),
                'fail_bg_colr': settings_data.get('fail_bg_colr'),
                'fail_txt_colr': settings_data.get('fail_txt_colr'),
                'prgs_icon_id': settings_data.get('prgs_icon_id'),
                'prgs_bg_colr': settings_data.get('prgs_bg_colr'),
                'prgs_txt_colr': settings_data.get('prgs_txt_colr'),
                'nodt_icon_id': settings_data.get('nodt_icon_id'),
                'nodt_bg_colr': settings_data.get('nodt_bg_colr'),
                'nodt_txt_colr': settings_data.get('nodt_txt_colr'),
                'schd_icon_id': settings_data.get('schd_icon_id'),
                'schd_bg_colr': settings_data.get('schd_bg_colr'),
                'schd_txt_colr': settings_data.get('schd_txt_colr'),
                'regr_id': settings_data.get('regr_id'),
                'updr_id': settings_data.get('updr_id'),
                'grp_prgs_icon_id': settings_data.get('grp_prgs_icon_id'),
                'grp_sucs_icon_id': settings_data.get('grp_sucs_icon_id')
            }

            with self.conn.cursor() as cursor:
                cursor.execute(query, params)
                new_id = cursor.lastrowid
            
            return new_id
        except Exception as e:
            self.logger.error(f"DAO: Failed to create schedule settings: {e}", exc_info=True)
            raise