SELECT
    status AS error_code,
    COUNT(*) AS count
FROM tb_con_hist
{where_clause}
GROUP BY status
ORDER BY count DESC
