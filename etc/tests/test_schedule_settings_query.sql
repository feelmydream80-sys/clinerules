-- This script is for testing the SELECT query on the tb_data_clt_schd_sett table.
-- It creates the table, inserts sample data, and runs the query.

-- 1. Drop the table if it exists to ensure a clean test environment.
DROP TABLE IF EXISTS tb_data_clt_schd_sett;

-- 2. Create the table structure based on the DDL file.
-- Note: The column is correctly named `upd_dt`.
CREATE TABLE tb_data_clt_schd_sett (
    sett_id SERIAL PRIMARY KEY,
    grp_min_cnt INT,
    prgs_rt_red_thrsval NUMERIC,
    prgs_rt_org_thrsval NUMERIC,
    use_yn CHAR(1),
    sucs_icon_id INT,
    sucs_bg_colr VARCHAR(7),
    sucs_txt_colr VARCHAR(7),
    fail_icon_id INT,
    fail_bg_colr VARCHAR(7),
    fail_txt_colr VARCHAR(7),
    prgs_icon_id INT,
    prgs_bg_colr VARCHAR(7),
    prgs_txt_colr VARCHAR(7),
    nodt_icon_id INT,
    nodt_bg_colr VARCHAR(7),
    nodt_txt_colr VARCHAR(7),
    schd_icon_id INT,
    schd_bg_colr VARCHAR(7),
    schd_txt_colr VARCHAR(7),
    regr_id VARCHAR(255),
    regr_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updr_id VARCHAR(255),
    upd_dt TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Insert sample data to test the query.
-- Insert an older record.
INSERT INTO tb_data_clt_schd_sett (
    grp_min_cnt, prgs_rt_red_thrsval, prgs_rt_org_thrsval, use_yn,
    sucs_icon_id, sucs_bg_colr, sucs_txt_colr,
    fail_icon_id, fail_bg_colr, fail_txt_colr,
    prgs_icon_id, prgs_bg_colr, prgs_txt_colr,
    nodt_icon_id, nodt_bg_colr, nodt_txt_colr,
    schd_icon_id, schd_bg_colr, schd_txt_colr,
    regr_id, updr_id, upd_dt
) VALUES (
    5, 30.0, 60.0, 'Y',
    1, '#28a745', '#ffffff',
    2, '#dc3545', '#ffffff',
    3, '#ffc107', '#000000',
    4, '#6c757d', '#ffffff',
    5, '#17a2b8', '#ffffff',
    'test_user', 'test_user', '2025-11-26 10:00:00'
);

-- Insert a more recent record, which should be the one returned by the query.
INSERT INTO tb_data_clt_schd_sett (
    grp_min_cnt, prgs_rt_red_thrsval, prgs_rt_org_thrsval, use_yn,
    sucs_icon_id, sucs_bg_colr, sucs_txt_colr,
    fail_icon_id, fail_bg_colr, fail_txt_colr,
    prgs_icon_id, prgs_bg_colr, prgs_txt_colr,
    nodt_icon_id, nodt_bg_colr, nodt_txt_colr,
    schd_icon_id, schd_bg_colr, schd_txt_colr,
    regr_id, updr_id, upd_dt
) VALUES (
    10, 25.0, 75.0, 'Y',
    1, '#00ff00', '#ffffff',
    2, '#ff0000', '#ffffff',
    3, '#ffff00', '#000000',
    4, '#aaaaaa', '#ffffff',
    5, '#0000ff', '#ffffff',
    'test_user_2', 'test_user_2', '2025-11-26 11:00:00' -- Newer timestamp
);

-- 4. Run the query to be tested (with the corrected column name 'upd_dt').
-- This should return the second record (sett_id = 2).
SELECT
    sett_id,
    grp_min_cnt,
    prgs_rt_red_thrsval,
    prgs_rt_org_thrsval,
    use_yn,
    sucs_icon_id,
    sucs_bg_colr,
    sucs_txt_colr,
    fail_icon_id,
    fail_bg_colr,
    fail_txt_colr,
    prgs_icon_id,
    prgs_bg_colr,
    prgs_txt_colr,
    nodt_icon_id,
    nodt_bg_colr,
    nodt_txt_colr,
    schd_icon_id,
    schd_bg_colr,
    schd_txt_colr
FROM
    tb_data_clt_schd_sett
ORDER BY
    upd_dt DESC, sett_id DESC
LIMIT 1;