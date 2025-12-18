-- 카드 요약
UPDATE TB_MENU SET MENU_URL = '/card_summary' WHERE MENU_URL = 'card_summary.card_summary_page';

-- 차트 분석
UPDATE TB_MENU SET MENU_URL = '/chart-analysis' WHERE MENU_URL = 'analysis.chart_analysis_page';

-- 데이터 분석
UPDATE TB_MENU SET MENU_URL = '/data-analysis' WHERE MENU_URL = 'analysis.data_analysis_page';

-- 데이터 사양
UPDATE TB_MENU SET MENU_URL = '/data-spec' WHERE MENU_URL = 'data_spec.data_spec_page';

-- 잔디
UPDATE TB_MENU SET MENU_URL = '/jandi' WHERE MENU_URL = 'jandi.jandi_page';

-- 매핑 관리
UPDATE TB_MENU SET MENU_URL = '/mapping' WHERE MENU_URL = 'mapping.mapping_page';

-- 원시 데이터
UPDATE TB_MENU SET MENU_URL = '/raw_data' WHERE MENU_URL = 'raw_data.raw_data_page';
