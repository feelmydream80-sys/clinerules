CREATE TABLE tb_user_data_perm_auth_ctrl (
    USER_ID VARCHAR(20) NOT NULL,
    JOB_ID VARCHAR(50) NOT NULL,
    REG_DTM TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (USER_ID, JOB_ID)
);

COMMENT ON TABLE tb_user_data_perm_auth_ctrl IS '사용자별 데이터 접근 권한을 관리하는 테이블';
COMMENT ON COLUMN tb_user_data_perm_auth_ctrl.USER_ID IS '사용자 ID (TB_USER.USER_ID 참조)';
COMMENT ON COLUMN tb_user_data_perm_auth_ctrl.JOB_ID IS '접근 가능한 데이터의 JOB ID (TB_CLT_SCHD_DISP_SETT.JOB_ID 참조)';
COMMENT ON COLUMN tb_user_data_perm_auth_ctrl.REG_DTM IS '등록일시';