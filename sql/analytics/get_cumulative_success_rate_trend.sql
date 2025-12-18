WITH daily_stats AS (
    SELECT
        DATE(start_dt AT TIME ZONE 'Asia/Seoul') AS date,
        job_id,
        COUNT(*) AS total_count,
        SUM(CASE WHEN status = 'CD901' THEN 1 ELSE 0 END) AS success_count
    FROM
        tb_con_hist
    {where_clause}
    GROUP BY
        DATE(start_dt AT TIME ZONE 'Asia/Seoul'),
        job_id
),
cumulative_stats AS (
    SELECT
        date,
        job_id,
        SUM(total_count) OVER (PARTITION BY job_id ORDER BY date) AS cumulative_total,
        SUM(success_count) OVER (PARTITION BY job_id ORDER BY date) AS cumulative_success
    FROM
        daily_stats
)
SELECT
    date,
    job_id,
    (cumulative_success::FLOAT / cumulative_total::FLOAT) * 100 AS success_rate
FROM
    cumulative_stats
ORDER BY
    date,
    job_id;
