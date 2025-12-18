from datetime import datetime, timedelta
from typing import Optional
import pytz
from flask import current_app

def is_within_schedule_grace_period(
    schedule_dt_aware: datetime, 
    history_dt_utc: Optional[datetime], 
    grace_minutes: int = 5
) -> bool:
    """
    예정된 시간(schedule_dt_aware)과 실제 기록된 시간(history_dt_utc)을 비교하여
    허용 오차 시간(grace_minutes) 내에 있는지 확인합니다.

    - history_dt_utc가 없으면 False를 반환합니다.
    - 시간대(KST)를 고려하여 두 시간의 절대적인 차이를 비교합니다.
    """
    if not history_dt_utc:
        return False

    kst = pytz.timezone('Asia/Seoul')
    
    # history_dt가 timezone 정보가 없으면 UTC로 설정
    if history_dt_utc.tzinfo is None:
        history_dt_utc = pytz.utc.localize(history_dt_utc)
        
    history_dt_kst = history_dt_utc.astimezone(kst)

    # 시간 차이가 허용 범위 내에 있는지 확인
    time_diff = abs(schedule_dt_aware - history_dt_kst)
    is_within_grace = time_diff <= timedelta(minutes=grace_minutes)
    current_app.logger.debug(f"Comparing schedule {schedule_dt_aware} with history {history_dt_kst}. "
                         f"Time diff: {time_diff}, Grace period: {grace_minutes} mins. Match: {is_within_grace}")
    return is_within_grace