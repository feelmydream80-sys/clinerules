from typing import Optional, Dict, List
from sql.jandi.jandi_sql import get_daily_job_counts


class JandiMapper:
    def __init__(self, conn):
        self.conn = conn

    def get_daily_job_counts(self, job_id: Optional[str], start_date: Optional[str], end_date: Optional[str], all_data: bool, job_ids: Optional[List[str]] = None) -> List[Dict]:
        """잔디 메뉴용 일별 작업 성공 실행 건수 조회"""
        query, params = get_daily_job_counts(job_id, start_date, end_date, all_data, job_ids)
        with self.conn.cursor() as cur:
            cur.execute(query, params)
            columns = [desc[0] for desc in cur.description]
            results = [dict(zip(columns, row)) for row in cur.fetchall()]
            return results
