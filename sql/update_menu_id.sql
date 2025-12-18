-- 최고 관리자 메뉴의 menu_id를 'admin'에서 'mngr_sett'으로 수정합니다.
-- 이는 frontend router가 올바른 JavaScript 파일을 로드하기 위해 필요합니다.
UPDATE TB_MENU SET MENU_ID = 'mngr_sett' WHERE MENU_ID = 'admin';
