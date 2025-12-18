SELECT
    TO_CHAR(MIN(start_dt AT TIME ZONE 'Asia/Seoul'), 'YYYY-MM-DD') AS min_date,
    TO_CHAR(MAX(start_dt AT TIME ZONE 'Asia/Seoul'), 'YYYY-MM-DD') AS max_date
FROM tb_con_hist
