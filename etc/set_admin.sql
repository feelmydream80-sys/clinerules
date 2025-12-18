-- 'admin' 사용자에게 'mngr_sett' 메뉴 접근 권한을 부여하여 관리자로 설정합니다.
INSERT INTO tb_user_auth_ctrl (user_id, menu_id)
SELECT 'admin', 'mngr_sett'
WHERE NOT EXISTS (
    SELECT 1
    FROM tb_user_auth_ctrl
    WHERE user_id = 'admin' AND menu_id = 'mngr_sett'
);
