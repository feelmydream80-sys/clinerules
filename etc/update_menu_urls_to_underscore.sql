-- Change existing URLs from hyphen to underscore
UPDATE TB_MENU SET MENU_URL = '/chart_analysis' WHERE MENU_URL = '/chart-analysis';
UPDATE TB_MENU SET MENU_URL = '/data_analysis' WHERE MENU_URL = '/data-analysis';
UPDATE TB_MENU SET MENU_URL = '/data_report' WHERE MENU_URL = '/data-report';
UPDATE TB_MENU SET MENU_URL = '/data_spec' WHERE MENU_URL = '/data-spec';
UPDATE TB_MENU SET MENU_URL = '/mapping_management' WHERE MENU_URL = '/mapping-management';
UPDATE TB_MENU SET MENU_URL = '/mngr_sett' WHERE MENU_URL = '/mngr-sett';
UPDATE TB_MENU SET MENU_URL = '/card_summary' WHERE MENU_URL = '/card-summary';

-- Add/update the new collection schedule URL
-- Assuming the menu_id for '데이터 수집 일정표' is 'collection_schedule'
-- This will update if exists, or do nothing if it doesn't.
-- A separate INSERT statement might be needed if the menu item doesn't exist,
-- but for now, we focus on fixing existing links.
UPDATE TB_MENU SET MENU_URL = '/collection_schedule' WHERE menu_id = 'collection_schedule';
