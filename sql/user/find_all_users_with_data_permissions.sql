-- 사용자 목록과 각 사용자의 데이터 접근 권한(Job ID)을 조회합니다.
-- 검색어가 있는 경우 사용자 ID 또는 이름으로 필터링합니다.
SELECT
    A.USER_ID,
    A.USER_ID AS USER_NM,
    A.ACC_STS AS USER_STAT,
    COALESCE((
        SELECT
            '[' || STRING_AGG('"' || B.JOB_ID || '"', ',') || ']'
        FROM
            TB_USER_DATA_PERM_AUTH_CTRL B
        WHERE
            B.USER_ID = A.USER_ID
    ), '[]') AS JOB_IDS
FROM
    TB_USER A
-- {{search_sql}}
ORDER BY
    A.USER_ID;