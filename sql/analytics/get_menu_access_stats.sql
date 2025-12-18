SELECT
    m.MENU_ID,
    m.MENU_NM,
    COUNT(ual.USER_ID) AS total_access_count,
    COUNT(DISTINCT ual.USER_ID) AS unique_user_count
FROM
    TB_USER_ACS_LOG ual
JOIN
    TB_MENU m ON ual.MENU_NM = m.MENU_NM
{where_clause}
GROUP BY
    m.MENU_ID, m.MENU_NM
ORDER BY
    total_access_count DESC;
