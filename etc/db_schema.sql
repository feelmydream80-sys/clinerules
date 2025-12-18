-- Table structure for tb_col_mapp
CREATE TABLE IF NOT EXISTS tb_col_mapp (
    clm_mapp_id SERIAL PRIMARY KEY,
    src_clm_nm VARCHAR(255),
    tgt_clm_nm VARCHAR(255),
    tgt_clm_desc TEXT,
    tgt_clm_data_type VARCHAR(50)
);

-- Table structure for tb_con_hist
CREATE TABLE IF NOT EXISTS tb_con_hist (
    con_hist_id SERIAL PRIMARY KEY,
    con_id VARCHAR(255),
    con_dt TIMESTAMP,
    con_sts_cd VARCHAR(50),
    con_err_cd VARCHAR(50),
    con_err_msg TEXT,
    con_job_id VARCHAR(255)
);

-- Table structure for tb_con_mst
CREATE TABLE IF NOT EXISTS tb_con_mst (
    con_id VARCHAR(255) PRIMARY KEY,
    con_nm VARCHAR(255),
    con_desc TEXT,
    con_type VARCHAR(50),
    con_pd_cd VARCHAR(50)
);

-- Table structure for tb_con_trbl_hist
CREATE TABLE IF NOT EXISTS tb_con_trbl_hist (
    trbl_hist_id SERIAL PRIMARY KEY,
    con_id VARCHAR(255),
    trbl_dt TIMESTAMP,
    trbl_msg TEXT
);

-- Table structure for tb_data_spec
CREATE TABLE IF NOT EXISTS tb_data_spec (
    spec_id SERIAL PRIMARY KEY,
    data_nm VARCHAR(255),
    src_sys VARCHAR(255),
    data_desc TEXT,
    src_db_type VARCHAR(50),
    src_db_nm VARCHAR(255),
    src_tbl_nm VARCHAR(255),
    user_id VARCHAR(255),
    user_pwd VARCHAR(255)
);

-- Table structure for tb_data_spec_parm
CREATE TABLE IF NOT EXISTS tb_data_spec_parm (
    parm_id SERIAL PRIMARY KEY,
    spec_id INTEGER,
    parm_nm VARCHAR(255),
    parm_val TEXT,
    parm_type VARCHAR(50)
);

-- Table structure for tb_icon
CREATE TABLE IF NOT EXISTS tb_icon (
    icon_id SERIAL PRIMARY KEY,
    icon_cd VARCHAR(255),
    icon_nm VARCHAR(255),
    icon_cont TEXT,
    icon_desc TEXT,
    disp_yn BOOLEAN
);

-- Table structure for TB_USER
CREATE TABLE IF NOT EXISTS TB_USER (
    user_id VARCHAR(255) PRIMARY KEY,
    user_pwd VARCHAR(255),
    acc_sts VARCHAR(50),
    acc_cre_dt TIMESTAMP,
    acc_apr_dt TIMESTAMP
);

-- Table structure for TB_USER_AUTH_CTRL
CREATE TABLE IF NOT EXISTS TB_USER_AUTH_CTRL (
    auth_id SERIAL PRIMARY KEY,
    user_id VARCHAR(255),
    menu_id VARCHAR(255),
    auth_yn BOOLEAN
);

-- Table structure for TB_MENU
CREATE TABLE IF NOT EXISTS TB_MENU (
    menu_id VARCHAR(255) PRIMARY KEY,
    menu_nm VARCHAR(255),
    menu_url VARCHAR(255),
    menu_order INTEGER
);
