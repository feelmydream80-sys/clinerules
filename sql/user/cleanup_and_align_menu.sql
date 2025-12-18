-- 1. Remove redundant and incorrect menu and permission entries (user already deleted one part)
DELETE FROM TB_USER_AUTH_CTRL WHERE MENU_ID = 'card_summary.card_summary_page';
DELETE FROM TB_MENU WHERE MENU_ID = 'card_summary.card_summary_page';

-- 2. Align 'admin' menu_id to 'mngr_sett' across tables in the correct order
-- First, update the referencing table
UPDATE TB_USER_AUTH_CTRL SET MENU_ID = 'mngr_sett' WHERE MENU_ID = 'admin';
-- Then, update the referenced table
UPDATE TB_MENU SET MENU_ID = 'mngr_sett' WHERE MENU_ID = 'admin';
