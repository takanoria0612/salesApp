# app/main.py
from flask import Blueprint, flash, render_template, current_app
from flask_login import login_required
import openpyxl
import os
from datetime import datetime
import logging

from app.utils.excel_utils import open_excel_file, read_excel_data

# ブループリントの作成
bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # データの初期化
    data = []
    total_price = 0.0
    total_purchase = 0.0

    # Excelファイルの存在をチェックし、結果を変数に格納
    EXCEL_FILE_PATH = current_app.config['EXCEL_FILE_PATH']
    file_exists = os.path.exists(EXCEL_FILE_PATH)

    if file_exists:
        try:
            # Excelファイルを開く
            workbook = open_excel_file(EXCEL_FILE_PATH)
                        
            # read_excel_data 関数を使用してデータを読み込む
            data, total_price, total_purchase = read_excel_data(workbook, current_year, current_month)
            
            total_price = int(total_price)
            total_purchase = int(total_purchase)

        except Exception as e:
            logging.error(f"Excelファイルの読み込み中にエラーが発生しました: {e}")
            flash('Excelファイルの読み込み中にエラーが発生しました。', 'error')
            file_exists = False  # ここでfile_existsを更新してはいけません
    else:
        error_message = "Excelファイルが見つかりません"
        logging.error(error_message)
        flash(error_message, "error_index")
        data, total_price, total_purchase = [], 0, 0  # デフォルト値を設定

    # file_exists の状態に関わらず、テンプレートに必要な変数を渡す
    return render_template('index.html', file_exists=file_exists, data=data, total_price=total_price, total_purchase=total_purchase)

