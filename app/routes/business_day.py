from flask import Blueprint, request, jsonify, current_app
import logging
from app.utils.excel_utils import find_data_by_date

business_day_bp = Blueprint('business_day', __name__)

@business_day_bp.route('/set-business-day', methods=['POST'])
def set_business_day():
    EXCEL_FILE_PATH = current_app.config['EXCEL_FILE_PATH']
    try:
        data = request.get_json()
        business_day = data.get('businessDay')
        print(business_day)
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

