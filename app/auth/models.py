from flask_login import UserMixin
from app.auth.repository import get_user_by_id

class User(UserMixin):
    def __init__(self, data):
        self.id = data["id"]
        self.username = data["username"]
        self.email = data["email"]
        self.is_admin = data.get("is_admin", False)
        self.is_active = data.get("is_active", False)

    @staticmethod
    def get(user_id):
        data = get_user_by_id(user_id)
        return User(data) if data else None
