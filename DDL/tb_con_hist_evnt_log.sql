-- Table: public.tb_con_hist_evnt_log

-- DROP TABLE IF EXISTS public.tb_con_hist_evnt_log;

CREATE TABLE IF NOT EXISTS public.tb_con_hist_evnt_log
(
    evnt_id integer NOT NULL DEFAULT nextval('tb_con_hist_event_log_id_seq'::regclass),
    evnt_tp character varying(10) COLLATE pg_catalog."default",
    evnt_occr_time timestamp with time zone DEFAULT now(),
    evnt_chg_row jsonb,
    CONSTRAINT tb_con_hist_event_log_pkey PRIMARY KEY (evnt_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.tb_con_hist_evnt_log
    OWNER to etl_user;