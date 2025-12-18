-- 특정 사용자의 데이터 접근 권한(Job ID 목록)을 조회합니다.
SELECT
    JOB_ID
FROM
    TB_USER_DATA_PERM_AUTH_CTRL
WHERE
    USER_ID = %(user_id)s
ORDER BY
    JOB_ID ASC;