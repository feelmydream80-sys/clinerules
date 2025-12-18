import logging
from dao.icon_dao import IconDAO

class IconMapper:
    
    def __init__(self, db_connection):
        self.icon_dao = IconDAO(db_connection)
        self.logger = logging.getLogger(self.__class__.__name__)

    def get_all_icons(self):
        return self.icon_dao.get_all_icons()

    def get_icon_by_code(self, icon_code):
        return self.icon_dao.get_icon_by_code(icon_code)

    def insert_icon(self, icon_data):
        return self.icon_dao.insert_icon(icon_data)

    def update_icon(self, icon_data):
        return self.icon_dao.update_icon(icon_data)

    def insert_or_update_icon(self, icon_data):
        if icon_data.get('ICON_ID'):
            self.logger.info(f"Mapper: Updating icon with ID {icon_data['ICON_ID']}")
            return self.update_icon(icon_data)
        else:
            self.logger.info(f"Mapper: Inserting new icon with code {icon_data.get('ICON_CD')}")
            return self.insert_icon(icon_data)

    def delete_icon(self, icon_id):
        return self.icon_dao.delete_icon(icon_id)

    def toggle_icon_display(self, icon_id, display_yn):
        return self.icon_dao.update_icon_display_status(icon_id, display_yn)


    def delete_all_icons(self):
        return self.icon_dao.delete_all_icons()
