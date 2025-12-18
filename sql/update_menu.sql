-- 메뉴 테이블(tb_menu)에 기본 메뉴 항목들을 추가합니다.
-- 이미 존재하는 항목은 무시합니다.

-- 대시보드
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order)
SELECT 'dashboard', '대시보드', '/dashboard', 1
WHERE NOT EXISTS (SELECT 1 FROM tb_menu WHERE menu_id = 'dashboard');

-- 잔디
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order)
SELECT 'jandi', '잔디', '/jandi', 2
WHERE NOT EXISTS (SELECT 1 FROM tb_menu WHERE menu_id = 'jandi');

-- 원본 데이터
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order)
SELECT 'raw_data', '원본 데이터', '/raw_data', 3
WHERE NOT EXISTS (SELECT 1 FROM tb_menu WHERE menu_id = 'raw_data');

-- 차트 분석
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order)
SELECT 'chart_analysis', '차트 분석', '/chart_analysis', 4
WHERE NOT EXISTS (SELECT 1 FROM tb_menu WHERE menu_id = 'chart_analysis');

-- 데이터 분석
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order)
SELECT 'data_analysis', '데이터 분석', '/data_analysis', 5
WHERE NOT EXISTS (SELECT 1 FROM tb_menu WHERE menu_id = 'data_analysis');

-- 데이터 명세서
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order)
SELECT 'data_spec', '데이터 명세서', '/data_spec', 6
WHERE NOT EXISTS (SELECT 1 FROM tb_menu WHERE menu_id = 'data_spec');

-- API 테스트
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order)
SELECT 'api_test', 'API 테스트', '/api_test', 7
WHERE NOT EXISTS (SELECT 1 FROM tb_menu WHERE menu_id = 'api_test');

-- 관리자 설정 (is_admin 권한용)
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order)
SELECT 'admin', '관리자 설정', '/mngr_sett', 8
WHERE NOT EXISTS (SELECT 1 FROM tb_menu WHERE menu_id = 'admin');

-- Airflow
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order)
SELECT 'airflow', 'Airflow', '/airflow', 9
WHERE NOT EXISTS (SELECT 1 FROM tb_menu WHERE menu_id = 'airflow');

-- Kafka UI
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order)
SELECT 'kafka_ui', 'Kafka UI', '/kafka_ui', 10
WHERE NOT EXISTS (SELECT 1 FROM tb_menu WHERE menu_id = 'kafka_ui');
