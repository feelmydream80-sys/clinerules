SELECT
    MIN((start_dt AT TIME ZONE 'Asia/Seoul')::date) AS min_date,
    MAX((start_dt AT TIME ZONE 'Asia/Seoul')::date) AS max_date
FROM tb_con_hist;
