"""TB_API_KEY_MNGR 서비스 레이어"""

from dao.api_key_mngr_dao import ApiKeyMngrDao
from dao.con_mst_dao import ConMstDAO
from datetime import datetime
from msys.database import get_db_connection
import logging

class ApiKeyMngrService:
    """TB_API_KEY_MNGR 서비스 클래스"""

    def __init__(self):
        """Initialize ApiKeyMngrService"""
        self.dao = ApiKeyMngrDao()
        self.logger = logging.getLogger(__name__)

    def get_all_api_key_mngr(self):
        """Get all API key manager records with expiry information"""
        try:
            data = self.dao.select_all()
            
            # Convert dates and calculate expiry info
            result = []
            today = datetime.now().date()
            
            for item in data:
                if isinstance(item['start_dt'], str):
                    item['start_dt'] = datetime.strptime(item['start_dt'], '%Y-%m-%d').date()
                
                expiry_dt = datetime(item['start_dt'].year + item['due'], item['start_dt'].month, item['start_dt'].day).date() if item['start_dt'] else None
                days_remaining = (expiry_dt - today).days if expiry_dt else 0
                
                item['start_dt'] = item['start_dt'].isoformat() if item['start_dt'] else None
                item['expiry_dt'] = expiry_dt.isoformat() if expiry_dt else None
                item['days_remaining'] = days_remaining
                item['is_expiring_soon'] = days_remaining <= 30
                
                result.append(item)
            
            # Sort by start date (descending)
            result.sort(key=lambda x: x['start_dt'], reverse=True)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting API key manager data: {e}")
            raise

    def update_cd_from_mngr_sett(self):
        """Update CD values in TB_API_KEY_MNGR from TB_MNGR_SETT"""
        try:
            added_cds = []
            updated_cds = []
            
            # Get all CD values from TB_MNGR_SETT not in TB_API_KEY_MNGR
            conn = get_db_connection()
            cds_not_in_api_key_mngr = self.dao.select_cds_not_in_api_key_mngr(conn)
            
            # Add each CD to TB_API_KEY_MNGR with data from TB_CON_MST
            for cd_item in cds_not_in_api_key_mngr:
                cd = cd_item['cd']
                
                try:
                    # Get ITEM10 and UDATE_DT from TB_CON_MST
                    con_mst_dao = ConMstDAO(conn)
                    con_mst_data = con_mst_dao.get_mst_data_by_cd(cd)
                    
                    if con_mst_data:
                        self.dao.insert(
                            cd=cd,
                            due=1,  # Default due is 1 year
                            start_dt=con_mst_data['udate_dt'],
                            api_ownr_email_addr='',  # Empty string instead of None
                            conn=conn
                        )
                        added_cds.append(cd)
                    else:
                        self.logger.warning(f"No CON_MST data found for CD: {cd}")
                
                except Exception as e:
                    self.logger.error(f"Error processing CD {cd}: {e}")
            
            return {'added_cds': added_cds, 'updated_cds': updated_cds}
            
        except Exception as e:
            self.logger.error(f"Error updating CD values: {e}")
            raise
    
    def update_api_key_mngr_with_api_key(self, cd, due, start_dt, api_ownr_email_addr, api_key):
        """Update API key manager data including API key in TB_CON_MST"""
        try:
            conn = get_db_connection()
            
            # Update TB_API_KEY_MNGR
            self.dao.update(cd, due, start_dt, api_ownr_email_addr, conn)
            
            # Update TB_CON_MST ITEM10 with API key
            con_mst_dao = ConMstDAO(conn)
            con_mst_data = con_mst_dao.get_mst_data_by_cd(cd)
            
            if con_mst_data:
                # Update only ITEM10
                update_data = {
                    'item10': api_key
                }
                # Since cd_cl is required for update, we need to find it
                # First, let's get all columns from con_mst_data to preserve existing values
                full_update_data = {**con_mst_data, **update_data}
                con_mst_dao.update_mst_data(con_mst_data['cd_cl'], cd, full_update_data)
            
            conn.commit()
            self.logger.debug(f"Successfully updated API key manager and API key for CD: {cd}")
            return True
            
        except Exception as e:
            if 'conn' in locals():
                conn.rollback()
            self.logger.error(f"Error updating API key manager with API key: {e}")
            raise
