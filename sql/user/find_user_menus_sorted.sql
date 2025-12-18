-- 사용자가 접근 가능한 메뉴 목록을 메뉴 순서(menu_order)에 따라 정렬하여 반환합니다.
SELECT
    m.menu_id,
    m.menu_nm,
    m.menu_url,
    m.menu_order
FROM
    tb_menu m
JOIN
    tb_user_auth_ctrl a ON m.menu_id = a.menu_id
WHERE
    a.user_id = %s
ORDER BY
    m.menu_order ASC;
