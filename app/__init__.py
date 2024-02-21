from flask import Flask
from flask_login import LoginManager
from config import Config
from app.models import User

# Flask-Loginの設定
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'ログインしてください。'

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    # Flask-Loginの初期化
    login_manager.init_app(app)

    # ブループリントのインポート
    from app.main import bp
    from app.users import user_bp
    from app.routes import auth_bp
    from app.routes import data_management_bp
    from app.routes import business_day_bp
    # ブループリントの登録
    app.register_blueprint(bp, url_prefix='/')
    app.register_blueprint(user_bp, url_prefix="/user")
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(data_management_bp)
    app.register_blueprint(business_day_bp)
    return app
