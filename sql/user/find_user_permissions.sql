-- 사용자의 모든 메뉴 접근 권한을 조회합니다.
SELECT a.menu_id
FROM tb_user_auth_ctrl a
WHERE a.user_id = %s;
