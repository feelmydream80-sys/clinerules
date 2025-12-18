DELETE FROM tb_menu WHERE menu_id = 'card_summary';
INSERT INTO tb_menu (menu_id, menu_nm, menu_url, menu_order) VALUES ('card_summary', '카드 요약', '/card_summary', 1);
