-- Initial data for TB_USER
INSERT INTO TB_USER (user_id, user_pwd, acc_sts, acc_cre_dt, acc_apr_dt) VALUES
('etl_user', '0anH/1WcNrXbVhvLMzYsnA==$q21pFFWQurf0K//Dkdix83BNIzWs0lfbhUKn3g4D7Rmcy/j1oe3b/PeRe4/jUwNI4cY2goApxLPglxwxE5mG+w==', 'APPROVED', '2025-10-16 15:44:00.815675+09:00', NULL),
('admin', 'roPTKJgC3yglP+EJDY0AUA==$/racN6MNoXqxC16CpA7afji62X5n5hmXg6keNFUXGqWwShSwAetbFSiq9+xDnZYd9Z8FHEd1tGJJlP4d7+t2IQ==', 'APPROVED', '2025-09-18 14:18:34.419796+09:00', '2025-09-18 14:18:34.419796+09:00');

-- Initial data for TB_USER_AUTH_CTRL
INSERT INTO TB_USER_AUTH_CTRL (auth_id, user_id, menu_id, auth_yn) VALUES
(159, 'etl_user', 'dashboard', TRUE),
(177, 'admin', 'card_summary', TRUE),
(178, 'admin', 'jandi', TRUE),
(180, 'admin', 'dashboard', TRUE),
(181, 'admin', 'raw_data', TRUE),
(182, 'admin', 'data_spec', TRUE),
(183, 'admin', 'data_analysis', TRUE),
(184, 'admin', 'chart_analysis', TRUE),
(185, 'etl_user', 'card_summary', TRUE),
(1, 'admin', 'mngr_sett', TRUE);

-- Initial data for TB_MENU
INSERT INTO TB_MENU (menu_id, menu_nm, menu_url, menu_order) VALUES
('dashboard', '대시보드', '/dashboard', 2),
('airflow', 'Airflow', 'http://10.200.153.136:180', 10),
('kafka_ui', 'Kafka UI', 'http://10.200.153.136:28080/', 11),
('api_test', 'API 테스트', '/api_test', 9),
('chart_analysis', '차트분석', '/chart-analysis', 5),
('data_analysis', '데이터분석', '/data-analysis', 4),
('data_spec', '데이터 명세서', '/data-spec', 7),
('jandi', '잔디', '/jandi', 3),
('raw_data', '상세데이터', '/raw_data', 6),
('card_summary', '카드 요약', '/card_summary', 1),
('mngr_sett', '관리자 설정', '/mngr_sett', 8);
