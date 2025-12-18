-- Step 1: Create a new 'mngr_sett' menu item by copying the 'admin' item.
-- This ensures the foreign key target exists before we update permissions.
INSERT INTO TB_MENU (MENU_ID, MENU_NM, MENU_URL, PRNTS_MENU_ID, LVL, SORT_ORDR, USE_YN, RGST_DT, RGST_ID, MDFY_DT, MDFY_ID)
SELECT 'mngr_sett', MENU_NM, MENU_URL, PRNTS_MENU_ID, LVL, SORT_ORDR, USE_YN, RGST_DT, RGST_ID, MDFY_DT, MDFY_ID
FROM TB_MENU
WHERE MENU_ID = 'admin';

-- Step 2: Update the permissions table to point to the new 'mngr_sett' menu_id.
UPDATE TB_USER_AUTH_CTRL SET MENU_ID = 'mngr_sett' WHERE MENU_ID = 'admin';

-- Step 3: Delete the old 'admin' menu item, which is no longer referenced.
DELETE FROM TB_MENU WHERE MENU_ID = 'admin';

-- Clean up the incorrect card_summary entry as well
DELETE FROM TB_USER_AUTH_CTRL WHERE MENU_ID = 'card_summary.card_summary_page';
DELETE FROM TB_MENU WHERE MENU_ID = 'card_summary.card_summary_page';
