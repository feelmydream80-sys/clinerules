SELECT
    MENU_NM,
    COUNT(*) AS access_count
FROM
    TB_USER_ACS_LOG
{where_clause}
GROUP BY
    MENU_NM
ORDER BY
    access_count DESC
