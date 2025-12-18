-- 모든 사용자에게 'card_summary' 메뉴에 대한 기본 권한을 부여합니다.
-- 이미 권한이 있는 사용자는 무시합니다.
INSERT INTO TB_USER_AUTH_CTRL (USER_ID, MENU_ID, auth_yn)
SELECT USER_ID, 'card_summary', true
FROM TB_USER
WHERE NOT EXISTS (
    SELECT 1
    FROM TB_USER_AUTH_CTRL
    WHERE TB_USER_AUTH_CTRL.USER_ID = TB_USER.USER_ID
    AND TB_USER_AUTH_CTRL.MENU_ID = 'card_summary'
);
