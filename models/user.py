from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_id, permissions=None):
        self.id = user_id
        self.permissions = permissions or []
