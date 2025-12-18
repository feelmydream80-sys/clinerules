-- tb_clt_schd_disp_sett 테이블 구조 변경
-- 그룹 외곽선 스타일, 색상 기준, 성공률 임계값 컬럼 추가
ALTER TABLE tb_clt_schd_disp_sett 
ADD COLUMN grp_brdr_styl VARCHAR(20),
ADD COLUMN grp_colr_crtr VARCHAR(10),
ADD COLUMN succ_rt_red_thrsval INTEGER,
ADD COLUMN succ_rt_org_thrsval INTEGER;

-- 기존 데이터에 대한 기본값 설정 (옵션)
-- UPDATE tb_clt_schd_disp_sett SET grp_brdr_styl = 'solid', grp_colr_crtr = 'prgr', succ_rt_red_thrsval = 30, succ_rt_org_thrsval = 60 WHERE sett_id IS NOT NULL;