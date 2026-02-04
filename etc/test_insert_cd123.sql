-- tb_con_mst에 CD123 데이터 추가 테스트
INSERT INTO tb_con_mst (cd_cl, cd, cd_nm, cd_desc, item1, item2, item3, item4, item5, item6, item7, item8, item9, item10)
VALUES ('CD001', 'CD123', '테스트 작업', '테스트 작업 설명', '값1', '값2', '값3', '값4', '값5', '값6', '값7', '값8', '값9', '값10');

-- tb_mngr_sett에 자동 생성된 설정 확인
SELECT * FROM tb_mngr_sett WHERE cd = 'CD123';