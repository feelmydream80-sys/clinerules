WITH current_year_daily AS (
    SELECT
        DATE_TRUNC('day', ACS_DT) AS access_date,
        MENU_NM,
        COUNT(USER_ID) AS daily_total_access,
        COUNT(DISTINCT USER_ID) AS daily_unique_users
    FROM TB_USER_ACS_LOG
    {where_clause}
    GROUP BY access_date, MENU_NM
),
current_year_weekly AS (
    SELECT
        EXTRACT(MONTH FROM access_date)::integer AS month,
        FLOOR((EXTRACT(DAY FROM access_date) + EXTRACT(DOW FROM DATE_TRUNC('month', access_date)) - 2) / 7) + 1 AS week_of_month,
        MENU_NM,
        SUM(daily_total_access) AS total_access_count,
        SUM(daily_unique_users) AS unique_user_count
    FROM current_year_daily
    GROUP BY month, week_of_month, MENU_NM
),
last_year_daily AS (
    SELECT
        DATE_TRUNC('day', ACS_DT) AS access_date,
        MENU_NM,
        COUNT(USER_ID) AS daily_total_access,
        COUNT(DISTINCT USER_ID) AS daily_unique_users
    FROM TB_USER_ACS_LOG
    {last_year_where_clause}
    GROUP BY access_date, MENU_NM
),
last_year_weekly AS (
    SELECT
        EXTRACT(MONTH FROM access_date)::integer AS month,
        FLOOR((EXTRACT(DAY FROM access_date) + EXTRACT(DOW FROM DATE_TRUNC('month', access_date)) - 2) / 7) + 1 AS week_of_month,
        MENU_NM,
        SUM(daily_total_access) AS last_year_total_access_count,
        SUM(daily_unique_users) AS last_year_unique_user_count
    FROM last_year_daily
    GROUP BY month, week_of_month, MENU_NM
)
SELECT
    COALESCE(cy.month, ly.month) as month,
    COALESCE(cy.week_of_month, ly.week_of_month) as week_of_month,
    m.MENU_ID,
    COALESCE(cy.MENU_NM, ly.MENU_NM) as MENU_NM,
    COALESCE(cy.total_access_count, 0) as total_access_count,
    COALESCE(cy.unique_user_count, 0) as unique_user_count,
    COALESCE(ly.last_year_total_access_count, 0) as last_year_total_access_count,
    COALESCE(ly.last_year_unique_user_count, 0) as last_year_unique_user_count
FROM
    current_year_weekly cy
FULL OUTER JOIN
    last_year_weekly ly ON cy.month = ly.month AND cy.week_of_month = ly.week_of_month AND cy.MENU_NM = ly.MENU_NM
JOIN
    TB_MENU m ON COALESCE(cy.MENU_NM, ly.MENU_NM) = m.MENU_NM
ORDER BY
    month, week_of_month;
