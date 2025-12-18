-- Step 1: Create a new 'mngr_sett' menu item using only known columns.
INSERT INTO TB_MENU (MENU_ID, MENU_NM, MENU_URL)
SELECT 'mngr_sett', MENU_NM, MENU_URL
FROM TB_MENU
WHERE MENU_ID = 'admin';

-- Step 2: Update the permissions table to point to the new 'mngr_sett' menu_id.
UPDATE TB_USER_AUTH_CTRL SET MENU_ID = 'mngr_sett' WHERE MENU_ID = 'admin';

-- Step 3: Delete the old 'admin' menu item, which is no longer referenced.
DELETE FROM TB_MENU WHERE MENU_ID = 'admin';

-- Clean up the incorrect card_summary entry as well
DELETE FROM TB_USER_AUTH_CTRL WHERE MENU_ID = 'card_summary.card_summary_page';
DELETE FROM TB_MENU WHERE MENU_ID = 'card_summary.card_summary_page';
