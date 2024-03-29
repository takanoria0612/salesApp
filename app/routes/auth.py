from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User
import logging

logger = logging.getLogger(__name__)
auth_bp = Blueprint("auth", __name__, static_folder='static', template_folder='templates')
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.authenticate(username, password)
        if user:
            login_user(user)
            logger.info(f"ユーザー名 '{username}' のログインに成功しました。")
            return redirect(url_for('main.index'))

    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    # ログアウトするユーザーの名前を取得
    username = current_user.username
    logout_user()
    
    logger.info(f"ユーザー名 '{username}' がログアウトしました。")
    return redirect(url_for('main.index'))