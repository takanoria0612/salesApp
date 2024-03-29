from flask import Blueprint, request, jsonify, current_app
import logging
from app.utils.excel_utils import find_data_by_date
import requests
from datetime import date, timedelta

logger = logging.getLogger(__name__)

business_day_bp = Blueprint('business_day', __name__)

@business_day_bp.route('/set-business-day', methods=['POST'])
def set_business_day():
    EXCEL_FILE_PATH = current_app.config['EXCEL_FILE_PATH']
    try:
        data = request.get_json()
        business_day = data.get('businessDay')

        if not business_day:
            logging.error("Business day not provided in the request.")
            return jsonify({'status': 'error', 'message': 'Business day is required.'}), 400

        # Excelファイルを検索するロジック
        excel_data = find_data_by_date(EXCEL_FILE_PATH, business_day)
        if excel_data and excel_data['exists']:
            logging.info(f" {business_day} のデータは既に存在します")
            return jsonify({'status': 'success', 'data': excel_data})
        else:
            logging.info(f"{business_day}のデータは存在しません。追加してください")
            return jsonify({'status': 'not found', 'message': "前営業日のデータはありません。新しいデータを追加してください"})

    except Exception as e:
        logging.error(f"Error while setting business day: {e}", exc_info=True)
        return jsonify({'status': 'error', 'message': 'An error occurred while processing your request.'}), 500



def fetch_public_holidays(year):
    """Fetch public holidays for the given year."""
    try:
        response = requests.get(f'https://holidays-jp.github.io/api/v1/{year}/date.json')
        response.raise_for_status()  # Raises stored HTTPError, if one occurred.
        holidays = response.json()
        logger.debug(f"祝日のリスト: {holidays}")
        return [date.fromisoformat(day) for day in holidays]
    except Exception as e:
        logger.error(f"Error fetching public holidays: {e}")
        return []

from datetime import date, timedelta, datetime

def calculate_business_days_for_filter(year, month, holidays):
    """Calculate business days up to the specified date, excluding weekends and public holidays."""
    start_date = date(year, month, 1)
    today = datetime.now().date()
    # 月末の日付を計算する
    if month == 12:
        end_date = date(year + 1, 1, 1) - timedelta(days=1)
    else:
        end_date = date(year, month + 1, 1) - timedelta(days=1)

    logger.debug(f"end_date: {end_date}")
    current_business_day = fetch_public_holidays(year)

    business_days = 0
    logger.debug(f"祝日のリスト: {holidays}")
    while start_date <= end_date:
        # 土日（weekday 0-4 が月曜日から金曜日）でない、かつ祝日でない場合にカウント
        if start_date.weekday() < 5 and start_date not in holidays:
            business_days += 1
        start_date += timedelta(days=1)

    return business_days

def calculate_business_days_to_date(year, month, holidays):
    """Calculate business days up to the specified date, excluding weekends and public holidays."""
    start_date = date(year, month, 1)
    today = datetime.now().date()
    # 現在の月と年を確認し、異なる場合は月末を計算の終了日とする
    end_date = today if today.month == month and today.year == year else date(year, month + 1, 1) - timedelta(days=1)

    current_business_day = fetch_public_holidays(year)
    business_days = 0

    while start_date < end_date:
        # 土日（weekday 0-4 が月曜日から金曜日）でない、かつ祝日でない場合にカウント
        if start_date.weekday() < 5 and start_date not in holidays:
            business_days += 1
        start_date += timedelta(days=1)

    return business_days