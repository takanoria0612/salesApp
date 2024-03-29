# app/main.py
from flask import Blueprint, flash, render_template, current_app
from flask_login import login_required
import os
from datetime import date, datetime
import logging
from app.routes.business_day import calculate_business_days_to_date, fetch_public_holidays
from app.utils.excel_utils import open_excel_file, read_excel_data
from app.models import ExcelDataRow
from datetime import datetime


# ロガーの取得
logger = logging.getLogger(__name__)
# ブループリントの作成
bp = Blueprint('main', __name__)

@bp.route('/')
@login_required
def index():
    logger.debug("index関数が呼び出されました。")
    now = datetime.now()
    current_year = now.year
    current_month = now.month
    today_date = now.date()
    # データの初期化
    data = []
    total_price = 0.0
    total_purchase = 0.0
    sales_average = 0.0
    total_price_until_today = 0.0  # 今日までの合計価格
    # Excelファイルの存在をチェックし、結果を変数に格納
    EXCEL_FILE_PATH = current_app.config['EXCEL_FILE_PATH']
    file_exists = os.path.exists(EXCEL_FILE_PATH)

    if file_exists:
        try:
            # Excelファイルを開く
            workbook = open_excel_file(EXCEL_FILE_PATH)
            # read_excel_data 関数を使用してデータを読み込む
            raw_data, total_price, total_purchase = read_excel_data(workbook, current_year, current_month)
            

            rows = []
            for row in raw_data:
                excel_data_row = ExcelDataRow(
                    date=row[0],  # 日付
                    sets=row[1],  # セット数
                    customers=row[2],  # 顧客数
                    bowls=row[3],  # ボウル数
                    purchase_total=row[4],  # 購入合計
                    cash_total=row[5],  # 現金合計
                    card_total=row[6],  # カード合計
                    rakuten_pay=row[7],  # 楽天ペイ
                    paypay=row[8],  # PayPay
                    usd_total=row[9],  # USD合計
                    total_price=row[10],  # 合計価格
                    remarks=''  # 備考
                )
                rows.append(excel_data_row)
                
            # 今日までのtotal_priceを計算
            total_price_until_today = ExcelDataRow.calculate_total_price_until_date(rows, today_date)
            # read_excel_data 関数を使用してデータを読み込む
            data, total_price, total_purchase = read_excel_data(workbook, current_year, current_month)
            total_purchase = int(total_purchase)
            
            # 今月の公休日を取得
            public_holidays = fetch_public_holidays(current_year)
            # 営業日数を計算
            business_days = calculate_business_days_to_date(current_year, current_month, public_holidays)
            # 月平均売上を計算（営業日数が0の場合は0で除算しないようにする）
            logger.debug(f"business_days: {business_days}")
            if business_days > 0:
            # 月の平均売上を計算し、小数第一位まで丸める
                sales_average = round(total_price_until_today / business_days, 1)
                logger.debug(f"今月の本日以前の営業日は{business_days}日です。現時点での売り上げ平均は{sales_average}円です。")
            else:
                sales_average = 0.0
                logger.info("今月の本日以前の営業日数は0日です。現時点での売り上げ平均は0円になります。")
        except Exception as e:
            logger.error(f"Excelファイルの読み込み中にエラーが発生しました: {e}")
            flash('Excelファイルの読み込み中にエラーが発生しました。', 'error')
            business_days = 1  # デフォルト値
            file_exists = False  # ここでfile_existsを更新してはいけません
    else:
        error_message = "Excelファイルが見つかりません"
        logger.error(error_message)
        flash(error_message, "error_index")
        data, total_price, total_purchase = [], 0, 0  # デフォルト値を設定

    # file_exists の状態に関わらず、テンプレートに必要な変数を渡す
    return render_template('index.html', file_exists=file_exists, data=data, total_price=total_price, total_purchase=total_purchase, sales_average=sales_average, business_days=business_days)

