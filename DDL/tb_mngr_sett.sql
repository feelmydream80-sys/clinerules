-- Table: public.tb_mngr_sett

-- DROP TABLE IF EXISTS public.tb_mngr_sett;

CREATE TABLE IF NOT EXISTS public.tb_mngr_sett
(
    cd character varying(50) COLLATE pg_catalog."default" NOT NULL,
    cnn_failr_thrs_val integer DEFAULT 3,
    cnn_warn_thrs_val integer DEFAULT 2,
    cnn_failr_icon_id integer,
    cnn_failr_wrd_colr character varying(7) COLLATE pg_catalog."default" DEFAULT '#dc3545'::character varying,
    cnn_warn_icon_id integer,
    cnn_warn_wrd_colr character varying(7) COLLATE pg_catalog."default" DEFAULT '#ffc107'::character varying,
    cnn_sucs_icon_id integer,
    cnn_sucs_wrd_colr character varying(7) COLLATE pg_catalog."default" DEFAULT '#28a745'::character varying,
    dly_sucs_rt_thrs_val integer DEFAULT 80,
    dd7_sucs_rt_thrs_val integer DEFAULT 75,
    mthl_sucs_rt_thrs_val integer DEFAULT 70,
    mc6_sucs_rt_thrs_val integer DEFAULT 65,
    yy1_sucs_rt_thrs_val integer DEFAULT 60,
    sucs_rt_sucs_icon_id integer,
    sucs_rt_sucs_wrd_colr character varying(7) COLLATE pg_catalog."default" DEFAULT '#28a745'::character varying,
    sucs_rt_warn_icon_id integer,
    sucs_rt_warn_wrd_colr character varying(7) COLLATE pg_catalog."default" DEFAULT '#ffc107'::character varying,
    chrt_prd_value integer DEFAULT 1,
    chrt_tp character varying(20) COLLATE pg_catalog."default" DEFAULT 'line'::character varying,
    chrt_dsp_job_id text COLLATE pg_catalog."default",
    chrt_dsp_yn boolean DEFAULT true,
    chrt_colr character varying(7) COLLATE pg_catalog."default" DEFAULT '#42A5F5'::character varying,
    grass_chrt_min_colr character varying(7) COLLATE pg_catalog."default" DEFAULT '#9be9a8'::character varying,
    grass_chrt_max_colr character varying(7) COLLATE pg_catalog."default" DEFAULT '#216e39'::character varying,
    CONSTRAINT tb_admin_settings_pkey PRIMARY KEY (cd)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_mngr_sett
    OWNER to etl_user;


-- Trigger function to automatically insert default settings into tb_mngr_sett when a new record is inserted into tb_con_mst
CREATE OR REPLACE FUNCTION insert_mngr_sett_on_con_mst_insert()
RETURNS TRIGGER AS $$
DECLARE
    cd_number INTEGER;
BEGIN
    -- Check if settings already exist for the cd value in tb_mngr_sett
    IF NOT EXISTS (SELECT 1 FROM tb_mngr_sett WHERE cd = NEW.cd) THEN
        -- Check if cd starts with 'CD' followed by numbers
        IF NEW.cd LIKE 'CD%' AND LENGTH(NEW.cd) > 2 THEN
            -- Try to convert the part after 'CD' to a number
            BEGIN
                cd_number := SUBSTRING(NEW.cd, 3)::INTEGER;
                
                -- Skip insertion if:
                -- 1. The number is between 900 and 999 (CD900-CD999)
                -- 2. The number is divisible by 100 (100, 200, 300, ..., 1000, 1100, ...)
                IF (cd_number >= 900 AND cd_number <= 999) OR (cd_number % 100 = 0) THEN
                    RETURN NEW; -- Skip insertion for these special cases
                END IF;
            EXCEPTION 
                WHEN invalid_text_representation THEN
                    -- If conversion fails, continue with normal insertion
                    NULL;
            END;
        END IF;
        
        -- Insert default settings only if they don't already exist and don't match exclusion criteria
       wprk ecs_wrd_colr,
            dly_sucs_rt_thrs_val,
            dd7_sucs_rt_thrs_val,
            mthl_sucs_rt_thrs_val,
            mc6_sucs_rt_thrs_val,
            yy1_sucs_rt_thrs_val,
            sucs_rt_sucs_icon_id,
            sucs_rt_sucs_wrd_colr,
            sucs_rt_warn_icon_id,
            sucs_rt_warn_wrd_colr,
            chrt_colr,
            chrt_dsp_yn,
            grass_chrt_min_colr,
            grass_chrt_max_colr
        ) VALUES (
            NEW.cd,
            5,    -- CNN_FAILR_THRS_VAL
            3,    -- CNN_WARN_THRS_VAL
            2,    -- CNN_FAILR_ICON_ID
            '#dc3545',  -- CNN_FAILR_WRD_COLR
            5,    -- CNN_WARN_ICON_ID
            '#ffc107',  -- CNN_WARN_WRD_COLR
            1,    -- CNN_SUCS_ICON_ID
            '#28a745',  -- CNN_SUCS_WRD_COLR
            95, -- DLY_SUCS_RT_THRS_VAL
            90, -- DD7_SUCS_RT_THRS_VAL
            85, -- MTHL_SUCS_RT_THRS_VAL
            80, -- MC6_SUCS_RT_THRS_VAL
            75, -- YY1_SUCS_RT_THRS_VAL
            1,    -- SUCS_RT_SUCS_ICON_ID
            '#28a745',  -- SUCS_RT_SUCS_WRD_COLR
            5,    -- SUCS_RT_WARN_ICON_ID
            '#ffc107',  -- SUCS_RT_WARN_WRD_COLR
            '#007bff',  -- CHRT_COLR
            true, -- CHRT_DSP_YN (boolean type)
            '#9be9a8',  -- GRASS_CHRT_MIN_COLR
            '#216e39'   -- GRASS_CHRT_MAX_COLR
        );
    END IF;
    
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Trigger to detect INSERT events on tb_con_mst table
CREATE TRIGGER trg_after_insert_con_mst
    AFTER INSERT ON tb_con_mst
    FOR EACH ROW
    EXECUTE FUNCTION insert_mngr_sett_on_con_mst_insert();


-- Test and cleanup SQL statements
-- Test the trigger by inserting test records into tb_con_mst
-- Test case 1: CD910 (should be excluded as it's in the 900-999 range)
-- INSERT INTO tb_con_mst (cd_cl, cd, cd_nm, cd_desc, item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, update_dt, del_dt, use_yn) 
-- VALUES ('CD001', 'CD910', 'Test Job 910', 'Test Job Description 910', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7', 'value8', 'value9', 'value10', NOW(), NULL, 'Y');

-- Test case 2: CD1000 (should be excluded as it's divisible by 100)
-- INSERT INTO tb_con_mst (cd_cl, cd, cd_nm, cd_desc, item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, update_dt, del_dt, use_yn) 
-- VALUES ('CD001', 'CD1000', 'Test Job 1000', 'Test Job Description 1000', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7', 'value8', 'value9', 'value10', NOW(), NULL, 'Y');

-- Test case 3: CD1001 (should be included as it doesn't meet exclusion criteria)
-- INSERT INTO tb_con_mst (cd_cl, cd, cd_nm, cd_desc, item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, update_dt, del_dt, use_yn) 
-- VALUES ('CD001', 'CD1001', 'Test Job 1001', 'Test Job Description 1001', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7', 'value8', 'value9', 'value10', NOW(), NULL, 'Y');

-- Test case 4: CD123 (should be included as it doesn't meet exclusion criteria)
-- INSERT INTO tb_con_mst (cd_cl, cd, cd_nm, cd_desc, item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, update_dt, del_dt, use_yn) 
-- VALUES ('CD001', 'CD123', 'Test Job 123', 'Test Job Description 123', 'value1', 'value2', 'value3', 'value4', 'value5', 'value6', 'value7', 'value8', 'value9', 'value10', NOW(), NULL, 'Y');

-- Cleanup test data from both tables
-- DELETE FROM tb_mngr_sett WHERE cd IN ('CD910', 'CD1000', 'CD1001', 'CD123');
-- DELETE FROM tb_con_mst WHERE cd IN ('CD910', 'CD1000', 'CD1001', 'CD123');
