-- Table: public.tb_user_acs_log

-- DROP TABLE IF EXISTS public.tb_user_acs_log;

CREATE TABLE IF NOT EXISTS public.tb_user_acs_log
(
    user_log_id integer NOT NULL DEFAULT nextval('tb_user_access_log_log_id_seq'::regclass),
    user_id character varying(255) COLLATE pg_catalog."default" NOT NULL,
    menu_nm character varying(255) COLLATE pg_catalog."default" NOT NULL,
    acs_dt timestamp with time zone NOT NULL DEFAULT now(),
    CONSTRAINT tb_user_access_log_pkey PRIMARY KEY (user_log_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_user_acs_log
    OWNER to etl_user;