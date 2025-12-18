-- '카드 요약' 메뉴를 TB_MENU 테이블에 추가합니다.
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, is_external, is_active)
VALUES ('card_summary', '카드 요약', '/card_summary', false, true)
ON CONFLICT (menu_id) DO NOTHING;

-- 'admin' 사용자에게 '카드 요약' 메뉴 접근 권한을 부여합니다.
INSERT INTO tb_user_auth_ctrl (user_id, menu_id, is_active)
VALUES ('admin', 'card_summary', true)
ON CONFLICT (user_id, menu_id) DO NOTHING;
