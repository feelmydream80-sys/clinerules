import logging
from mapper.analysis_mapper import AnalysisMapper

from typing import Optional, Dict, List

class AnalysisService:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.mapper = AnalysisMapper(db_connection)
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_dynamic_chart_data(self, params: dict, user: Optional[Dict] = None) -> list[dict]:
        """
        요청 파라미터를 기반으로 동적 차트 데이터를 조회합니다.
        사용자 권한에 따라 조회 가능한 job_id를 필터링합니다.
        """
        try:
            self.logger.info(f"▶ Service: 동적 차트 데이터 요청: {params} for user: {user.get('user_id') if user else 'None'}")
            
            allowed_job_ids = self._get_allowed_job_ids(user, params.get('job_ids'))
            if allowed_job_ids is not None and not allowed_job_ids:
                self.logger.warning(f"User {user.get('user_id')} has no data permissions for requested jobs. Returning empty chart data.")
                return []
            
            params['job_ids'] = allowed_job_ids
            
            data = self.mapper.get_dynamic_chart_data(params)
            self.logger.info(f"✅ Service: 동적 차트 데이터 {len(data)}건 조회 성공")
            return data
        except ValueError as ve:
            self.logger.error(f"❌ Service: 유효하지 않은 파라미터: {ve}", exc_info=True)
            raise
        except Exception as e:
            self.logger.error(f"❌ Service: 동적 차트 데이터 조회 실패: {e}", exc_info=True)
            raise

    def _get_allowed_job_ids(self, user: Optional[Dict], requested_job_ids: Optional[List[str]] = None) -> Optional[List[str]]:
        if not user or 'mngr_sett' in user.get('permissions', []):
            return requested_job_ids

        user_permissions = set(user.get('data_permissions', []))
        if not user_permissions:
            return []

        if requested_job_ids:
            allowed = list(user_permissions.intersection(set(requested_job_ids)))
            logging.info(f"User requested {requested_job_ids}, allowed: {allowed}")
            return allowed
        
        return list(user_permissions)
