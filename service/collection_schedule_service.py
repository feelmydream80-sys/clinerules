from msys.database import get_db_connection
from mapper.mst_mapper import MstMapper
from mapper.user_mapper import UserMapper
from datetime import datetime, timedelta
import croniter
import pytz
import re
from typing import Optional, Dict, List
from flask import current_app
from utils.datetime_utils import is_within_schedule_grace_period

class CollectionScheduleService:
    def __init__(self, conn):
        self.conn = conn

    def get_schedule_and_history(self, start_date, end_date, user: Optional[Dict] = None) -> List[Dict]:
        """
        주어진 기간 동안의 데이터 수집 스케줄과 실제 이력을 조합하여 반환합니다.
        사용자 권한에 따라 표시되는 Job이 필터링됩니다.
        """
        # Import here to avoid circular import
        from service.dashboard_service import DashboardService
        dashboard_service = DashboardService(self.conn)
        mst_mapper = MstMapper(self.conn)
        
        allowed_job_ids = None
        if user:
            is_admin = 'mngr_sett' in user.get('permissions', [])
            if not is_admin:
                allowed_job_ids = user.get('data_permissions', [])
                if not allowed_job_ids:
                    return []

        kst = pytz.timezone('Asia/Seoul')
        now_kst = datetime.now(kst)

        all_mst_data = mst_mapper.get_all_mst_for_schedule(allowed_job_ids)
        jobs = {mst['cd']: mst.get('item6') for mst in all_mst_data if mst.get('item6')}

        scheduled_tasks = []
        current_date = start_date
        while current_date <= end_date:
            for cd, cron_str in jobs.items():
                if not cron_str or not re.match(r'^(\S+\s+){4,5}\S+$', cron_str.strip()):
                    continue

                try:
                    base_time = datetime(current_date.year, current_date.month, current_date.day)
                    cron = croniter.croniter(cron_str, base_time)
                    schedule_time = cron.get_next(datetime)
                    while schedule_time.date() == current_date:
                        schedule_time_aware = kst.localize(schedule_time)
                        status = "미수집"
                        if schedule_time_aware > now_kst:
                            status = "예정"

                        scheduled_tasks.append({
                            "date": schedule_time.strftime('%Y-%m-%d %H:%M:%S'),
                            "job_id": cd,
                            "cron": cron_str,
                            "status": status,
                        })
                        schedule_time = cron.get_next(datetime)
                except (ValueError, KeyError):
                    current_app.logger.warning(f"Skipping job '{cd}' due to invalid cron string: '{cron_str}'")
                    continue
                except Exception as e:
                    current_app.logger.error(f"Error parsing cron string '{cron_str}' for job '{cd}': {e}")
            current_date += timedelta(days=1)
        
        history_data = dashboard_service.get_collection_history_for_schedule_with_start_dt(start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'), allowed_job_ids, user=user)
        

        # history_data를 날짜와 job_id로 그룹화하여 쉽게 찾을 수 있도록 재구성합니다.
        history_by_date_job = {}
        for item in history_data:
            history_dt_utc = item.get('start_dt')
            if not history_dt_utc:
                continue
            
            if history_dt_utc.tzinfo is None:
                history_dt_utc = pytz.utc.localize(history_dt_utc)
            
            history_dt_kst = history_dt_utc.astimezone(kst)
            item['start_dt_kst'] = history_dt_kst # KST 시간 추가
            date_str = history_dt_kst.strftime('%Y-%m-%d')
            job_id = item['job_id']
            
            if date_str not in history_by_date_job:
                history_by_date_job[date_str] = {}
            if job_id not in history_by_date_job[date_str]:
                history_by_date_job[date_str][job_id] = []
            history_by_date_job[date_str][job_id].append(item)

        # scheduled_tasks를 순회하며 상태를 업데이트합니다.
        unmatched_history = []

        for task in scheduled_tasks:
            if task['status'] == '예정':
                continue

            try:
                schedule_dt = datetime.strptime(task['date'], '%Y-%m-%d %H:%M:%S')
                # KST timezone을 적용하여 timezone-aware datetime으로 변환
                schedule_dt = kst.localize(schedule_dt)
            except (ValueError, KeyError) as e:
                current_app.logger.error(f"Failed to parse schedule date for task {task.get('job_id', 'unknown')}: {e}")
                continue
            schedule_date_str = schedule_dt.strftime('%Y-%m-%d')
            job_id = task['job_id']

            # 해당 날짜와 Job ID에 맞는 history가 있는지 확인합니다.
            if schedule_date_str in history_by_date_job and job_id in history_by_date_job[schedule_date_str]:
                
                history_for_job = history_by_date_job[schedule_date_str][job_id]

                # 시간을 기준으로 정렬하여 가장 먼저 발생한 기록부터 확인
                history_for_job.sort(key=lambda x: x.get('start_dt_kst') or datetime.min.replace(tzinfo=kst))

                # 가장 먼저 발생한 성공/수집중 기록을 찾아 매칭합니다.
                best_match = None
                for item in history_for_job:
                    status_code = item.get('status')
                    if status_code in ['CD901', 'CD904', 'CD902', 'CD903']: # 모든 상태 코드 확인
                        best_match = item
                        break # 가장 빠른 기록을 찾았으므로 중단

                if best_match:
                    status_code = best_match.get('status')
                    if status_code == 'CD901':
                        task['status'] = '성공'
                    elif status_code == 'CD904':
                        task['status'] = '수집중'
                    elif status_code == 'CD902':
                        task['status'] = '실패'
                    elif status_code == 'CD903':
                        task['status'] = '미수집'
                    
                    task['actual_date'] = best_match['start_dt_kst'].strftime('%Y-%m-%d %H:%M:%S')
                    
                    # 매칭된 기록은 리스트에서 제거하여 중복 사용을 방지합니다.
                    history_for_job.remove(best_match)
        
        # 남은 기록들을 처리합니다. (스케줄 없이 수집된 경우)
        # 권한 체크: allowed_job_ids가 None이면 모든 Job 허용 (admin), 아니면 허용된 Job만
        allowed_job_set = None if allowed_job_ids is None else set(allowed_job_ids)
        
        for date_str, jobs in history_by_date_job.items():
            for job_id, history_list in jobs.items():
                # 권한 체크: 사용자에게 권한이 없는 Job은 건너뜀
                if allowed_job_set is not None and job_id not in allowed_job_set:
                    continue
                    
                for item in history_list:
                    kst_time = item['start_dt_kst']
                    status_code = item.get('status')

                    # 상태 코드에 따라 적절한 텍스트로 변환
                    if status_code == 'CD901':
                        status_text = '성공'
                    elif status_code == 'CD902':
                        status_text = '실패'
                    elif status_code == 'CD903':
                        status_text = '미수집'
                    elif status_code == 'CD904':
                        status_text = '수집중'
                    else:
                        status_text = '알 수 없음'

                    scheduled_tasks.append({
                        "date": kst_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "job_id": job_id,
                        "cron": "Unscheduled",
                        "status": status_text,
                        "actual_date": kst_time.strftime('%Y-%m-%d %H:%M:%S'),
                        "is_unscheduled": True
                    })

        return scheduled_tasks