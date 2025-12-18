SELECT
    (start_dt AT TIME ZONE 'Asia/Seoul')::date AS date,
    job_id,
    (SUM(CASE WHEN status = 'CD901' THEN 1 ELSE 0 END) * 100.0 / NULLIF(COUNT(*), 0)) AS success_rate
FROM tb_con_hist
{where_clause}
GROUP BY (start_dt AT TIME ZONE 'Asia/Seoul')::date, job_id
ORDER BY (start_dt AT TIME ZONE 'Asia/Seoul')::date, job_id;
