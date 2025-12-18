INSERT INTO tb_data_clt_schd_sett (
    grp_min_cnt, prgs_rt_red_thrsval, prgs_rt_org_thrsval, use_yn,
    grp_brdr_styl, grp_colr_crtr, succ_rt_red_thrsval, succ_rt_org_thrsval,
    sucs_icon_id, sucs_bg_colr, sucs_txt_colr,
    fail_icon_id, fail_bg_colr, fail_txt_colr,
    prgs_icon_id, prgs_bg_colr, prgs_txt_colr,
    nodt_icon_id, nodt_bg_colr, nodt_txt_colr,
    schd_icon_id, schd_bg_colr, schd_txt_colr,
    grp_prgs_icon_id, grp_sucs_icon_id,
    regr_id, updr_id, upd_dt
) VALUES (
    %(grp_min_cnt)s, %(prgs_rt_red_thrsval)s, %(prgs_rt_org_thrsval)s, %(use_yn)s,
    %(grp_brdr_styl)s, %(grp_colr_crtr)s, %(succ_rt_red_thrsval)s, %(succ_rt_org_thrsval)s,
    %(sucs_icon_id)s, %(sucs_bg_colr)s, %(sucs_txt_colr)s,
    %(fail_icon_id)s, %(fail_bg_colr)s, %(fail_txt_colr)s,
    %(prgs_icon_id)s, %(prgs_bg_colr)s, %(prgs_txt_colr)s,
    %(nodt_icon_id)s, %(nodt_bg_colr)s, %(nodt_txt_colr)s,
    %(schd_icon_id)s, %(schd_bg_colr)s, %(schd_txt_colr)s,
    %(grp_prgs_icon_id)s, %(grp_sucs_icon_id)s,
    %(regr_id)s, %(updr_id)s, CURRENT_TIMESTAMP
) RETURNING sett_id;