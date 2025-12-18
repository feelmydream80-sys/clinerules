from dao.sql_loader import load_sql

class DashboardSQL:
    @staticmethod
    def get_event_log():
        return load_sql('dashboard/get_event_log.sql')

    @staticmethod
    def get_event_log_min_max_dates():
        return load_sql('dashboard/get_event_log_min_max_dates.sql')

    @staticmethod
    def get_min_max_dates():
        return load_sql('dashboard/get_min_max_dates.sql')

    @staticmethod
    def insert_event_log():
        return load_sql('dashboard/insert_event_log.sql')

    @staticmethod
    def get_dashboard_summary(start_date, end_date, all_data, job_ids=None):
        # Base query with all conditional aggregations
        kst_date_expr = "(h.start_dt::timestamp AT TIME ZONE 'Asia/Seoul')::date"
        
        query = f"""
            SELECT
                h.job_id,
                m.cd_nm,
                m.item6 as frequency,
                MIN(h.start_dt) AS min_con_dt,
                MAX(h.start_dt) AS max_con_dt,
                COUNT(*) as total_count,
                -- Overall counts
                COUNT(CASE WHEN h.status = 'CD901' THEN 1 END) as overall_success_count,
                COUNT(CASE WHEN h.status = 'CD902' THEN 1 END) as overall_ing_count,
                COUNT(CASE WHEN h.status = 'CD903' THEN 1 END) as overall_fail_count,
                COUNT(CASE WHEN h.status = 'CD904' THEN 1 END) as overall_cd904_count,
                COUNT(CASE WHEN h.status = 'CD905' THEN 1 END) as overall_no_data_count,

                -- Daily counts (today in KST)
                COUNT(CASE WHEN h.status = 'CD901' AND {kst_date_expr} = CURRENT_DATE THEN 1 END) as day_success,
                COUNT(CASE WHEN h.status = 'CD902' AND {kst_date_expr} = CURRENT_DATE THEN 1 END) as day_ing_count,
                COUNT(CASE WHEN h.status = 'CD903' AND {kst_date_expr} = CURRENT_DATE THEN 1 END) as day_fail_count,
                COUNT(CASE WHEN h.status = 'CD905' AND {kst_date_expr} = CURRENT_DATE THEN 1 END) as day_no_data_count,

                -- Weekly counts (this week in KST)
                COUNT(CASE WHEN h.status = 'CD901' AND {kst_date_expr} >= date_trunc('week', CURRENT_DATE) THEN 1 END) as week_success,
                COUNT(CASE WHEN h.status = 'CD902' AND {kst_date_expr} >= date_trunc('week', CURRENT_DATE) THEN 1 END) as week_ing_count,
                COUNT(CASE WHEN h.status = 'CD903' AND {kst_date_expr} >= date_trunc('week', CURRENT_DATE) THEN 1 END) as week_fail_count,
                COUNT(CASE WHEN h.status = 'CD905' AND {kst_date_expr} >= date_trunc('week', CURRENT_DATE) THEN 1 END) as week_no_data_count,

                -- Monthly counts (this month in KST)
                COUNT(CASE WHEN h.status = 'CD901' AND {kst_date_expr} >= date_trunc('month', CURRENT_DATE) THEN 1 END) as month_success,
                COUNT(CASE WHEN h.status = 'CD902' AND {kst_date_expr} >= date_trunc('month', CURRENT_DATE) THEN 1 END) as month_ing_count,
                COUNT(CASE WHEN h.status = 'CD903' AND {kst_date_expr} >= date_trunc('month', CURRENT_DATE) THEN 1 END) as month_fail_count,
                COUNT(CASE WHEN h.status = 'CD905' AND {kst_date_expr} >= date_trunc('month', CURRENT_DATE) THEN 1 END) as month_no_data_count,

                -- Half-year counts (last 6 months in KST)
                COUNT(CASE WHEN h.status = 'CD901' AND {kst_date_expr} >= date_trunc('month', CURRENT_DATE) - INTERVAL '5 months' THEN 1 END) as half_success,
                COUNT(CASE WHEN h.status = 'CD902' AND {kst_date_expr} >= date_trunc('month', CURRENT_DATE) - INTERVAL '5 months' THEN 1 END) as half_ing_count,
                COUNT(CASE WHEN h.status = 'CD903' AND {kst_date_expr} >= date_trunc('month', CURRENT_DATE) - INTERVAL '5 months' THEN 1 END) as half_fail_count,
                COUNT(CASE WHEN h.status = 'CD905' AND {kst_date_expr} >= date_trunc('month', CURRENT_DATE) - INTERVAL '5 months' THEN 1 END) as half_no_data_count,

                -- Yearly counts (this year in KST)
                COUNT(CASE WHEN h.status = 'CD901' AND {kst_date_expr} >= date_trunc('year', CURRENT_DATE) THEN 1 END) as year_success,
                COUNT(CASE WHEN h.status = 'CD902' AND {kst_date_expr} >= date_trunc('year', CURRENT_DATE) THEN 1 END) as year_ing_count,
                COUNT(CASE WHEN h.status = 'CD903' AND {kst_date_expr} >= date_trunc('year', CURRENT_DATE) THEN 1 END) as year_fail_count,
                COUNT(CASE WHEN h.status = 'CD905' AND {kst_date_expr} >= date_trunc('year', CURRENT_DATE) THEN 1 END) as year_no_data_count,

                -- 연속 실패 계산 (최근 10번 실행 중 실패 횟수)
                COALESCE((
                    SELECT COUNT(*)
                    FROM (
                        SELECT status
                        FROM TB_CON_HIST h2
                        WHERE h2.job_id = h.job_id
                        ORDER BY h2.start_dt DESC
                        LIMIT 10
                    ) recent_runs
                    WHERE recent_runs.status IN ('CD902', 'CD903') -- 실패 상태들
                ), 0) as fail_streak
            FROM
                TB_CON_HIST h
            LEFT JOIN
                TB_CON_MST m ON h.job_id = m.cd
        """
        params = []
        conditions = []

        if not all_data:
            if start_date:
                conditions.append(f"{kst_date_expr} >= %s")
                params.append(start_date)
            if end_date:
                conditions.append(f"{kst_date_expr} <= %s")
                params.append(end_date)
        
        if job_ids:
            conditions.append("h.job_id = ANY(%s)")
            params.append(job_ids)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)
        
        query += " GROUP BY h.job_id, m.cd_nm, m.item6 ORDER BY h.job_id ASC"
            
        return query, params

    @staticmethod
    def get_daily_job_counts(job_id, start_date, end_date, all_data, job_ids=None):
        kst_date_expr = "(start_dt::timestamp AT TIME ZONE 'Asia/Seoul')::date"
        query = f"""
            SELECT
                {kst_date_expr} as date,
                COUNT(*) as count
            FROM
                TB_CON_HIST
        """
        params = []
        conditions = []

        if job_id:
            conditions.append("job_id = %s")
            params.append(job_id)

        if job_ids:
            conditions.append("job_id = ANY(%s)")
            params.append(job_ids)

        if not all_data:
            if start_date:
                conditions.append(f"{kst_date_expr} >= %s")
                params.append(start_date)
            if end_date:
                conditions.append(f"{kst_date_expr} <= %s")
                params.append(end_date)

        if conditions:
            query += " WHERE " + " AND ".join(conditions)

        query += f" GROUP BY {kst_date_expr} ORDER BY {kst_date_expr}"

        return query, params

    @staticmethod
    def get_collection_history_for_schedule(start_date, end_date, job_ids=None):
        kst_date_expr = "(h.start_dt::timestamp AT TIME ZONE 'Asia/Seoul')::date"
        query = f"""
            SELECT
                h.job_id,
                h.start_dt,
                h.status
            FROM
                TB_CON_HIST h
        """
        conditions = [f"{kst_date_expr} BETWEEN %s AND %s"]
        params = [start_date, end_date]

        if job_ids:
            conditions.append("h.job_id = ANY(%s)")
            params.append(job_ids)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        return query, params

    @staticmethod
    def get_collection_history_for_schedule_with_start_dt(start_date, end_date, job_ids=None):
        kst_date_expr = "(h.start_dt::timestamp AT TIME ZONE 'Asia/Seoul')::date"
        query = f"""
            SELECT
                h.job_id,
                {kst_date_expr} as collection_date,
                h.status,
                h.start_dt
            FROM
                TB_CON_HIST h
        """
        conditions = [f"{kst_date_expr} BETWEEN %s AND %s"]
        params = [start_date, end_date]

        if job_ids:
            conditions.append("h.job_id = ANY(%s)")
            params.append(job_ids)
        
        if conditions:
            query += " WHERE " + " AND ".join(conditions)
            
        return query, params
        
    @staticmethod
    def get_distinct_error_codes(start_date=None, end_date=None, all_data=False, job_ids=None):
        query = "SELECT DISTINCT status FROM TB_CON_HIST"
        params = []
        conditions = ["status IS NOT NULL", "status <> 'CD901'"]

        if not all_data:
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
            
        query += " ORDER BY status"
        
        return query, params

    @staticmethod
    def get_distinct_job_ids(job_ids=None):
        query = "SELECT DISTINCT job_id FROM tb_con_hist WHERE job_id IS NOT NULL"
        params = []
        
        if job_ids:
            query += " AND job_id = ANY(%s)"
            params.append(job_ids)
            
        query += " ORDER BY job_id"
        
        return query, params
