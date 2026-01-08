#!/usr/bin/env python3
"""
임시 테스트 파일: _ensure_settings_for_all_jobs_with_history 메소드 동작 확인
"""
import sys
import logging
sys.path.append('.')

from msys_app import create_app
from msys.database import get_db_connection
from service.mngr_sett_service import MngrSettService

# 로깅 설정
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_ensure_settings():
    """_ensure_settings_for_all_jobs_with_history 메소드 테스트"""
    logger.info("=== 테스트 시작: _ensure_settings_for_all_jobs_with_history ===")

    conn = None
    try:
        # DB 연결
        conn = get_db_connection()
        logger.info("DB 연결 성공")

        # 서비스 인스턴스 생성
        service = MngrSettService(conn)
        logger.info("MngrSettService 인스턴스 생성 성공")

        # 현재 DB 상태 확인
        cur = conn.cursor()

        # TB_CON_HIST 확인
        logger.info("=== TB_CON_HIST 상태 ===")
        cur.execute('SELECT job_id, COUNT(*) as count FROM TB_CON_HIST WHERE job_id IS NOT NULL GROUP BY job_id ORDER BY job_id')
        hist_data = cur.fetchall()
        for row in hist_data:
            logger.info(f"TB_CON_HIST - job_id: {row[0]}, count: {row[1]}")

        # TB_CON_MST 확인
        logger.info("=== TB_CON_MST 상태 ===")
        cur.execute('SELECT cd_cl, cd, cd_nm FROM TB_CON_MST ORDER BY cd_cl, cd')
        mst_data = cur.fetchall()
        for row in mst_data:
            logger.info(f"TB_CON_MST - cd_cl: {row[0]}, cd: {row[1]}, cd_nm: {row[2]}")

        # TB_MNGR_SETT 확인 (테스트 전)
        logger.info("=== TB_MNGR_SETT 상태 (테스트 전) ===")
        cur.execute('SELECT cd FROM TB_MNGR_SETT ORDER BY cd')
        sett_data_before = cur.fetchall()
        for row in sett_data_before:
            logger.info(f"TB_MNGR_SETT - cd: {row[0]}")

        # get_all_settings() 호출 - 이 안에서 _ensure_settings_for_all_jobs_with_history가 실행됨
        logger.info("=== get_all_settings() 호출 시작 ===")
        settings = service.get_all_settings()
        logger.info(f"get_all_settings() 완료. 반환된 설정 개수: {len(settings)}")

        # TB_MNGR_SETT 확인 (테스트 후)
        logger.info("=== TB_MNGR_SETT 상태 (테스트 후) ===")
        cur.execute('SELECT cd FROM TB_MNGR_SETT ORDER BY cd')
        sett_data_after = cur.fetchall()
        for row in sett_data_after:
            logger.info(f"TB_MNGR_SETT - cd: {row[0]}")

        # 결과 분석
        logger.info("=== 결과 분석 ===")
        before_count = len(sett_data_before)
        after_count = len(sett_data_after)
        logger.info(f"테스트 전 TB_MNGR_SETT 레코드 수: {before_count}")
        logger.info(f"테스트 후 TB_MNGR_SETT 레코드 수: {after_count}")

        if after_count > before_count:
            logger.info(f"✅ 성공: {after_count - before_count}개의 새 설정이 생성되었습니다.")
            new_settings = set(row[0] for row in sett_data_after) - set(row[0] for row in sett_data_before)
            logger.info(f"새로 생성된 job_id: {new_settings}")
        elif after_count == before_count:
            logger.info("⚠️  변경 없음: 설정이 생성되지 않았습니다.")
        else:
            logger.error("❌ 오류: 설정 레코드 수가 줄었습니다.")

        # 트랜잭션 커밋
        conn.commit()
        logger.info("트랜잭션 커밋 완료")

    except Exception as e:
        logger.error(f"테스트 중 오류 발생: {e}", exc_info=True)
        if conn:
            conn.rollback()
            logger.info("트랜잭션 롤백 완료")
    finally:
        if conn:
            conn.close()
            logger.info("DB 연결 종료")

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        test_ensure_settings()
