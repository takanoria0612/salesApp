# app/main.py
from flask import Blueprint, flash, render_template, current_app
from flask_login import login_required
import openpyxl
import os
from datetime import datetime
import logging

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
            workbook = openpyxl.load_workbook(EXCEL_FILE_PATH)
            sheet = workbook.active

            # Excelファイルからデータを読み込む
            for row in sheet.iter_rows(min_row=2, values_only=True):
                if isinstance(row[0], datetime):
                    row_date = row[0].date()
                else:
                    row_date = datetime.strptime(str(row[0]), "%Y-%m-%d").date()

                if row_date.year == current_year and row_date.month == current_month:
                    # 合計値段と客数を取得
                    total = float(row[8]) if row[8] else 0
                    customers = int(row[2]) if row[2] else 0
                    purchase = float(row[4]) if row[4] else 0
                    # 客単価を計算
                    avg_spend = total / customers if customers > 0 else 0
                    # データリストに行と客単価を追加
                    data.append(row + (avg_spend,))
                    total_price += total
                    total_purchase += purchase
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

    # file_exists の状態に関わらず、テンプレートに必要な変数を渡す
    return render_template('index.html', file_exists=file_exists, data=data, total_price=total_price, total_purchase=total_purchase)

