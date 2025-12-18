-- 트리거 함수 생성
CREATE OR REPLACE FUNCTION log_con_hist_changes()
RETURNS TRIGGER AS $$
BEGIN
    -- TG_OP 변수를 사용하여 작업 유형(INSERT, UPDATE)을 결정합니다.
    IF (TG_OP = 'INSERT') THEN
        INSERT INTO tb_con_hist_evnt_log (op_type, op_dt, row_data)
        VALUES ('INSERT', NOW(), row_to_json(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO tb_con_hist_evnt_log (op_type, op_dt, row_data)
        VALUES ('UPDATE', NOW(), row_to_json(NEW));
        RETURN NEW;
    END IF;
    RETURN NULL; -- DELETE의 경우 아무 작업도 하지 않음
END;
$$ LANGUAGE plpgsql;

-- 기존 트리거가 있다면 삭제
DROP TRIGGER IF EXISTS trg_log_con_hist_changes ON tb_con_hist;

-- 트리거 생성
CREATE TRIGGER trg_log_con_hist_changes
AFTER INSERT OR UPDATE ON tb_con_hist
FOR EACH ROW
EXECUTE FUNCTION log_con_hist_changes();
