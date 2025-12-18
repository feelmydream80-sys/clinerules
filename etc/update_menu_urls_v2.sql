-- 카드 요약
UPDATE TB_MENU SET MENU_URL = '/card_summary' WHERE MENU_URL = 'card_summary.card_summary';

-- 차트 분석
UPDATE TB_MENU SET MENU_URL = '/chart-analysis' WHERE MENU_URL = 'analysis.chart_analysis';

-- 데이터 분석
UPDATE TB_MENU SET MENU_URL = '/data-analysis' WHERE MENU_URL = 'analysis.data_analysis';
