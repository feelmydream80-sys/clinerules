from dao.sql_loader import load_sql
from datetime import datetime, timedelta
import pytz

class RawDataSQL:
    @staticmethod
    def get_min_max_dates():
        return load_sql('raw_data/get_min_max_dates.sql')

    @staticmethod
    def get_raw_data(start_date, end_date, job_ids, all_data, use_kst_today=False):
        query = "SELECT * FROM TB_CON_HIST"
        params = []
        conditions = []

        kst = pytz.timezone('Asia/Seoul')
        utc = pytz.utc

        if use_kst_today:
            now_kst = datetime.now(kst)
            start_of_day_kst = now_kst.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day_kst = start_of_day_kst + timedelta(days=1, microseconds=-1)
            
            start_of_day_utc = start_of_day_kst.astimezone(utc)
            end_of_day_utc = end_of_day_kst.astimezone(utc)
            
            conditions.append("start_dt BETWEEN %s AND %s")
            params.extend([start_of_day_utc, end_of_day_utc])
        elif not all_data:
            if start_date:
                start_dt_kst = kst.localize(datetime.strptime(start_date, '%Y-%m-%d'))
                start_dt_utc = start_dt_kst.astimezone(utc)
                conditions.append("start_dt >= %s")
                params.append(start_dt_utc)
            if end_date:
                end_dt_kst = kst.localize(datetime.strptime(end_date, '%Y-%m-%d') + timedelta(days=1, microseconds=-1))
                end_dt_utc = end_dt_kst.astimezone(utc)
                conditions.append("start_dt <= %s")
                params.append(end_dt_utc)

        if job_ids:
            conditions.append("job_id = ANY(%s)")
            params.append(job_ids)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " ORDER BY start_dt DESC"
            
        return query, params
