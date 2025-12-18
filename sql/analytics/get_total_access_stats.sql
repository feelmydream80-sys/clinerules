SELECT
    COUNT(*) as total_access_count,
    COUNT(DISTINCT USER_ID) as unique_user_count
FROM
    TB_USER_ACS_LOG
{where_clause}
