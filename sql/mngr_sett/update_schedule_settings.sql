-- sql/mngr_sett/update_schedule_settings.sql
UPDATE
    tb_data_clt_schd_sett
SET
    grp_min_cnt = %(grp_min_cnt)s,
    prgs_rt_red_thrsval = %(prgs_rt_red_thrsval)s,
    prgs_rt_org_thrsval = %(prgs_rt_org_thrsval)s,
    use_yn = %(use_yn)s,
    grp_brdr_styl = %(grp_brdr_styl)s,
    grp_colr_crtr = %(grp_colr_crtr)s,
    succ_rt_red_thrsval = %(succ_rt_red_thrsval)s,
    succ_rt_org_thrsval = %(succ_rt_org_thrsval)s,
    sucs_icon_id = %(sucs_icon_id)s,
    sucs_bg_colr = %(sucs_bg_colr)s,
    sucs_txt_colr = %(sucs_txt_colr)s,
    fail_icon_id = %(fail_icon_id)s,
    fail_bg_colr = %(fail_bg_colr)s,
    fail_txt_colr = %(fail_txt_colr)s,
    prgs_icon_id = %(prgs_icon_id)s,
    prgs_bg_colr = %(prgs_bg_colr)s,
    prgs_txt_colr = %(prgs_txt_colr)s,
    nodt_icon_id = %(nodt_icon_id)s,
    nodt_bg_colr = %(nodt_bg_colr)s,
    nodt_txt_colr = %(nodt_txt_colr)s,
    schd_icon_id = %(schd_icon_id)s,
    schd_bg_colr = %(schd_bg_colr)s,
    schd_txt_colr = %(schd_txt_colr)s,
    grp_prgs_icon_id = %(grp_prgs_icon_id)s,
    grp_sucs_icon_id = %(grp_sucs_icon_id)s,
    updr_id = %(updr_id)s,
    upd_dt = CURRENT_TIMESTAMP
WHERE
    sett_id = %(sett_id)s;