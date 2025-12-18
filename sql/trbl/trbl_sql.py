from typing import Optional, List, Tuple

class TrblSQL:
    @staticmethod
    def get_all_troubles_query(start_date: Optional[str], end_date: Optional[str]) -> Tuple[str, list]:
        query = "SELECT status as trbl_status, COUNT(*) as count FROM TB_CON_HIST WHERE status != 'CD901'"
        params = []
        if start_date:
            query += " AND start_dt >= %s"
            params.append(start_date)
        if end_date:
            query += " AND start_dt <= %s"
            params.append(end_date)
        query += " GROUP BY status"
        return query, params

    @staticmethod
    def get_trouble_hourly_query(start_date: Optional[str], end_date: Optional[str]) -> Tuple[str, list]:
        query = "SELECT EXTRACT(HOUR FROM start_dt) as hour, COUNT(*) as count FROM TB_CON_HIST WHERE status != 'CD901'"
        params = []
        if start_date:
            query += " AND start_dt >= %s"
            params.append(start_date)
        if end_date:
            query += " AND start_dt <= %s"
            params.append(end_date)
        query += " GROUP BY hour ORDER BY hour"
        return query, params

    @staticmethod
    def get_trouble_hourly_by_status_query(start_date: Optional[str], end_date: Optional[str], job_ids: Optional[List[str]]) -> Tuple[str, list]:
        query = "SELECT EXTRACT(HOUR FROM start_dt) as hour, status as trbl_status, COUNT(*) as count FROM TB_CON_HIST WHERE status != 'CD901'"
        params = []
        if start_date:
            query += " AND start_dt >= %s"
            params.append(start_date)
        if end_date:
            query += " AND start_dt <= %s"
            params.append(end_date)
        if job_ids:
            query += " AND job_id = ANY(%s)"
            params.append(job_ids)
        query += " GROUP BY hour, status ORDER BY hour, status"
        return query, params

    @staticmethod
    def success_rate_trend_by_job(start_date: Optional[str], end_date: Optional[str], job_ids: Optional[List[str]]) -> Tuple[str, list]:
        query = """
            SELECT
                DATE(start_dt) as log_dt,
                job_id,
                COUNT(CASE WHEN status = 'CD901' THEN 1 END) as success_count,
                COUNT(CASE WHEN status = 'CD902' THEN 1 END) as fail_count,
                COUNT(CASE WHEN status = 'CD903' THEN 1 END) as no_data_count
            FROM
                TB_CON_HIST
        """
        params = []
        conditions = []
        if start_date:
            conditions.append("start_dt >= %s")
            params.append(start_date)
        if end_date:
            conditions.append("start_dt <= %s")
            params.append(end_date)
        if job_ids:
            conditions.append("job_id = ANY(%s)")
            params.append(job_ids)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += " GROUP BY log_dt, job_id ORDER BY log_dt, job_id"
        return query, params
