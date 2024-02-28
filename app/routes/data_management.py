from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, current_app
from flask_login import login_user, logout_user, login_required, current_user
import openpyxl
import os
from datetime import datetime, timedelta
from app.utils.excel_utils import find_data_by_date, open_excel_file, save_data
from app.utils.email_utils import send_email_with_form_data
from app.utils.user_utils import load_user_from_env



data_management_bp = Blueprint('data_management', __name__)

@data_management_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    EXCEL_FILE_PATH = current_app.config['EXCEL_FILE_PATH']
    workbook = open_excel_file(EXCEL_FILE_PATH)
    sheet = workbook.active


    # 初期フォームデータの設定
    form_data = {
        'sets': '',
        'customers': '',
        'bowls': '',
        'purchase_total': '',
        'total_price': '',
        'cash_total': '',
        'card_total': '',
        'usd_total': '',
        'remarks': '',
    }
    if request.method == 'GET':
        customers_str = form_data.get('customers', '').strip()
        customers = int(customers_str) if customers_str.isdigit() else 1  # 数字のみの場合に変換、それ以外はデフォルト値1
        total_price_str = form_data.get('total_price', '').strip()
        total_price = float(total_price_str) if total_price_str.replace('.', '', 1).isdigit() else 0


    elif request.method == 'POST':
        form_data = request.form.to_dict(flat=True)  # Use flat=True to get a regular dict
        
        date_str = form_data['date']
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()  # 日付のみを含むdateオブジェクト

        # Excelファイル内のデータをチェックし、更新する行を探す
        try:
            update_row = None
            for row in sheet.iter_rows(min_row=2, values_only=False):
                row_date = row[0].value
                if isinstance(row_date, datetime):
                    row_date = row_date.date()
                if row_date == date_obj:
                    update_row = row
                    break

            if update_row:  # 既存のデータを更新
                # 各セルに新しい値を設定
                update_row[1].value = int(form_data.get('sets', 0))
                update_row[2].value = int(form_data.get('customers', 0))
                update_row[3].value = int(form_data.get('bowls', 0))
                update_row[4].value = float(form_data.get('purchase_total', 0))
                update_row[5].value = float(form_data.get('cash_total', 0))
                update_row[6].value = float(form_data.get('card_total', 0))
                update_row[7].value = float(form_data.get('usd_total', 0))
                update_row[8].value = float(form_data.get('total_price', 0))
                update_row[9].value = form_data.get('remarks', '')

                flash('データを更新しました。', 'success')
            else:  # 新しいデータを追加
                sheet.append([
                    date_obj,
                    int(form_data.get('sets', 0)),
                    int(form_data.get('customers', 0)),
                    int(form_data.get('bowls', 0)),
                    float(form_data.get('purchase_total', 0)),
                    float(form_data.get('total_price', 0)),
                    float(form_data.get('cash_total', 0)),
                    float(form_data.get('card_total', 0)),
                    float(form_data.get('usd_total', 0)),
                    form_data.get('remarks', ''),
                    # float(per_customer_price)  # 客単価を追加
                    # float(form_data.get('per_customer_price', 2))
                ])
                flash('新しいデータを追加しました。', 'success')

            workbook.save(EXCEL_FILE_PATH)


            email_sent = send_email_with_form_data(form_data)
            if email_sent:
                flash('メールを送信しました。','success')
                # return jsonify({'status': 'success', 'message': 'データを更新しました。'})
                return redirect(url_for('data_management.add'))  # メール送信後に適切なページにリダイレクト
            else:
                flash('メールの送信に失敗しました。', 'error')
            
        except ValueError as e:
            # ここでエラーメッセージとともにフォームページにリダイレクト
            flash(str(e), 'error')
            # ここでエラーメッセージとともにフォームページに値を渡してレンダリング
            return render_template('add.html', form_data=form_data)

    # add.htmlを表示
    return render_template('add.html', form_data=form_data)

@data_management_bp.route('/fetch-data-for-date')
@login_required
def fetch_data_for_date():
    EXCEL_FILE_PATH = current_app.config['EXCEL_FILE_PATH']
    selected_date = request.args.get('date')
    data = find_data_by_date(EXCEL_FILE_PATH, selected_date)
    if data:
        return jsonify(data)
    else:
        return jsonify({'exists': False})

@data_management_bp.route('/filter', methods=['GET'])
@login_required
def filter_data():
    selected_month = request.args.get('selectedMonth', '')  # デフォルト値を空文字列に設定
    EXCEL_FILE_PATH = current_app.config['EXCEL_FILE_PATH']
    file_exists = os.path.exists(EXCEL_FILE_PATH)  # ファイルの存在を確認

    if not file_exists:
        flash("Excelファイルが見つかりません。", "error")
        return redirect(url_for('main.index'))

    year, month = map(int, selected_month.split('-'))

    try:
        workbook = openpyxl.load_workbook(EXCEL_FILE_PATH)
        sheet = workbook.active
    except Exception as e:
        flash("Excelファイルを開く際にエラーが発生しました。", "error")
        return redirect(url_for('main.index'))

    filtered_data = []
    total_purchase = 0.0

    for row in sheet.iter_rows(min_row=2, values_only=True):
        if isinstance(row[0], datetime):
            row_date = row[0]
        else:
            try:
                row_date = datetime.strptime(row[0], "%Y-%m-%d")
            except ValueError:
                continue

        if row_date.year == year and row_date.month == month:
            total_sales = float(row[8]) if row[8] else 0
            customer_count = int(row[2]) if row[2] else 0
            purchase_amount = float(row[4]) if row[4] else 0
            total_purchase += purchase_amount
            average_spend_per_customer = total_sales / customer_count if customer_count > 0 else 0
            row_data_with_avg_spend = list(row) + [average_spend_per_customer]
            filtered_data.append(row_data_with_avg_spend)

    total_purchase = int(total_purchase)
    total_price = sum(row[8] for row in filtered_data if row[8])

    return render_template('index.html', file_exists=True, data=filtered_data, total_price=total_price, total_purchase=total_purchase, selected_month=selected_month)