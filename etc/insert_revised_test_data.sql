-- 기존 테스트 데이터 삭제 (선택 사항, 필요 시 주석 해제)
-- DELETE FROM tb_user_acs_log WHERE user_id LIKE 'test_user%';

-- ===================================================================================
-- 수정된 테스트 데이터: 집계 로직 검증용
-- - 동일 사용자가 동일 메뉴를 다른 날짜에 접속하는 경우 (월별/주별 순방문자 수 검증)
-- - 동일 사용자가 다른 메뉴를 동일 날짜에 접속하는 경우 (사이트 순방문자 수 검증)
-- ===================================================================================

-- 2024년 데이터
-- 2024년 10월: user1이 '대시보드'를 두 번 접속 (다른 날짜)
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '대시보드', '2024-10-01 10:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '대시보드', '2024-10-02 11:00:00');
-- 2024년 10월: user2가 같은 날 다른 메뉴 접속 (사이트 순방문자 수 확인용)
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_2', '대시보드', '2024-10-01 14:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_2', 'API 테스트', '2024-10-01 14:05:00');
-- 2024년 10월: user3의 단일 접속
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_3', '데이터분석', '2024-10-03 15:00:00');
-- 2024년 11월: user1이 '관리자 설정'을 두 번 접속 (다른 날짜)
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '관리자 설정', '2024-11-05 09:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '관리자 설정', '2024-11-06 09:30:00');
-- 기타 데이터
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_2', '잔디', '2024-11-10 13:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_3', '차트분석', '2024-12-01 16:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '상세데이터', '2024-12-20 10:00:00');


-- 2025년 데이터
-- 2025년 9월: user1이 '대시보드'를 세 번 접속 (다른 날짜)
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '대시보드', '2025-09-01 10:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '대시보드', '2025-09-02 11:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '대시보드', '2025-09-03 12:00:00');
-- 2025년 9월: user2가 같은 날 다른 메뉴 접속
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_2', 'API 테스트', '2025-09-01 14:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_2', '데이터 명세서', '2025-09-01 14:05:00');
-- 2025년 9월: user3의 단일 접속
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_3', '데이터분석', '2025-09-05 15:00:00');
-- 2025년 10월: user1이 '관리자 설정'을 두 번 접속 (같은 날) -> 순방문자 1로 집계되어야 함
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '관리자 설정', '2025-10-10 09:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '관리자 설정', '2025-10-10 14:00:00');
-- 기타 데이터
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_2', '잔디', '2025-10-15 13:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_3', '차트분석', '2025-11-01 16:00:00');
INSERT INTO tb_user_acs_log (user_id, menu_nm, acs_dt) VALUES ('test_user_1', '상세데이터', '2025-12-24 10:00:00');
