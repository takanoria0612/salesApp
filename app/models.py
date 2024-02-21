from flask_login import UserMixin, LoginManager
from app.utils.user_utils import load_user_from_env

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def authenticate(username, password):
        user = users.get(username)
        if user and user.password == password:
            return user
        return None

    @staticmethod
    def get(user_id):
        for user in users.values():
            if user.id == user_id:
                return user
        return None

# 環境変数からユーザーデータベースをロードし、User インスタンスを作成
user_data = load_user_from_env()
users = {username: User(user_info["id"], user_info["username"], user_info["password"]) for username, user_info in user_data.items()}

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)