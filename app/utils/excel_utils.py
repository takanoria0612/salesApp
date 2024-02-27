import openpyxl
from datetime import datetime

def find_data_by_date(excel_file_path, selected_date_str):
    try:
        workbook = openpyxl.load_workbook(excel_file_path)
        sheet = workbook.active
        selected_date = datetime.strptime(selected_date_str, '%Y-%m-%d').date()
        for row in sheet.iter_rows(min_row=2, values_only=True):
            row_date = row[0].date() if isinstance(row[0], datetime) else None
            if row_date == selected_date:
                # 一致したら、その行のデータを辞書形式で返す
                data = {
                    'exists': True,
                    'date': selected_date_str,  # 選択された日付
                    'sets': row[1],
                    'customers': row[2],
                    'bowls': row[3],
                    'purchase_total': row[4],
                    'cash_total': row[5],
                    'card_total': row[6],
                    'usd_total': row[7],
                    'total_price': row[8],
                    'remarks': row[9] if len(row) > 9 else ""  
                }
                return data
    except Exception as e:
        print(f"Error while processing Excel file: {e}")
    return {'exists': False}

def save_data(excel_file_path, data):
    try:
        workbook = openpyxl.load_workbook(excel_file_path)
        sheet = workbook.active
        sheet.append(data)
        workbook.save(excel_file_path)
    except Exception as e:
        print(f"Error while saving data to Excel file: {e}")


def open_excel_file(excel_file_path: str) -> openpyxl.workbook.workbook.Workbook:
    """Excelファイルを開く"""
    return openpyxl.load_workbook(excel_file_path)