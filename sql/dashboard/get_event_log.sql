SELECT
    (EVNT_CHG_ROW ->> 'con_id')::text AS con_id,
    EVNT_OCCR_TIME AS start_dt,
    (EVNT_CHG_ROW ->> 'end_dt')::timestamptz AS end_dt,
    (EVNT_CHG_ROW ->> 'job_id')::text AS job_id,
    (EVNT_CHG_ROW ->> 'rqs_info')::text AS rqs_info,
    (EVNT_CHG_ROW ->> 'status')::text AS status
FROM TB_CON_HIST_EVNT_LOG
{where_clause}
ORDER BY EVNT_OCCR_TIME DESC
