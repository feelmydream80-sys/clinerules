-- 그룹 외곽선 스타일을 저장하기 위해 tb_clt_schd_disp_sett 테이블에 컬럼을 추가합니다.
-- VARCHAR(20)은 'solid', 'dashed', 'dotted', 'double' 등의 값을 저장하기에 충분합니다.
-- 기본값으로 'solid'를 설정합니다.
ALTER TABLE tb_clt_schd_disp_sett
ADD COLUMN grp_brdr_styl VARCHAR(20) DEFAULT 'solid';