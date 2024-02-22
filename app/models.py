import logging
from flask import flash
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
        logging.basicConfig(level=logging.DEBUG)
        user_database = load_user_from_env()
        print(username, password, 'def authenticate')
        logging.debug(f"Loaded user database: {user_database}")
        for user_id, user_data in user_database.items():
            if user_data['username'] == username:
                if user_data['password'] == password:
                    logging.debug(f"Authenticated user: {username}")
                    return User(user_data['id'], username, password)
                else:
                    flash("ログインに失敗しました", 'error')
                    logging.debug(f"Password mismatch for user: {username}")
                    return None

        flash("ログインに失敗しました", 'error')
        logging.debug(f"User not found: {username}")
        return None


    @staticmethod
    def get(user_id):
        user_database = load_user_from_env()
        for user_info in user_database.values():
            if user_info['id'] == user_id:
                return User(user_info['id'], user_info['username'], user_info['password'])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
