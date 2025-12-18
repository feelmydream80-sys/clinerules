import logging
from sql.analytics.analytics_sql import AnalyticsSQL

class AnalysisMapper:
    def __init__(self, db_connection):
        self.conn = db_connection
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_dynamic_chart_data(self, params: dict) -> list[dict]:
        """
        동적으로 생성된 쿼리를 실행하여 분석 차트 데이터를 반환합니다.
        """
        try:
            with self.conn.cursor() as cur:
                query, query_params = AnalyticsSQL.build_dynamic_query(params)
                self.logger.info(f"▶ Mapper: Executing dynamic query: {query} with params: {query_params}")
                cur.execute(query, query_params)
                columns = [desc[0].lower() for desc in cur.description]
                data = [dict(zip(columns, row)) for row in cur.fetchall()]
                self.logger.info(f"✅ Mapper: Fetched {len(data)} rows from dynamic query.")
                return data
        except Exception as e:
            self.logger.error(f"❌ Mapper: 동적 차트 데이터 조회 실패: {e}", exc_info=True)
            raise
