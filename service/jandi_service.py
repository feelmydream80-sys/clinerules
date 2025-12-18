import logging
from typing import Optional, Dict, List
from mapper.jandi_mapper import JandiMapper


class JandiService:
    def __init__(self, conn):
        self.conn = conn
        self.jandi_mapper = JandiMapper(conn)

    def get_daily_job_counts(self, job_id: Optional[str], start_date: Optional[str], end_date: Optional[str], all_data: bool, user: Optional[Dict] = None) -> List[Dict]:
        """잔디 메뉴용 일별 작업 성공 실행 건수 조회 (CD901, CD902 상태만 카운트)"""
        allowed_job_ids = None
        if user:
            is_admin = 'mngr_sett' in user.get('permissions', [])
            user_id = user.get('user_id', 'Unknown')
            logging.info(f"Checking data permissions for user: {user_id}, is_admin: {is_admin} in jandi get_daily_job_counts")
            if not is_admin:
                allowed_job_ids = user.get('data_permissions', [])
                logging.info(f"Non-admin user in jandi get_daily_job_counts. Applying data permissions. Allowed jobs: {allowed_job_ids}")
                if not allowed_job_ids:
                    logging.warning(f"User {user_id} has no data permissions. Returning empty daily job counts.")
                    return []
            else:
                logging.info(f"Admin user {user_id} in jandi get_daily_job_counts. No data permission filtering applied.")

        data = self.jandi_mapper.get_daily_job_counts(job_id, start_date, end_date, all_data, job_ids=allowed_job_ids)
        return data
