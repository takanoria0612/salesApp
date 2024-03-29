
# app/utils/validators.py
from datetime import datetime
from typing import Tuple
def validate_date(date_str):
    """日付がYYYY-MM-DD形式であり、過去または現在の日付であることを検証する"""

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        if date_obj.date() > datetime.today().date():
            return False, "未来の日付は使用できません。"
        return True, None
    except ValueError:
        return False, "無効な日付形式です。YYYY-MM-DD形式を使用してください。"


def validate_positive_or_zero(value):
    """Check if the value is a non-negative integer."""
    try:
        return int(value) >= 0
    except ValueError:
        return False

def validate_sets_greater_than_customers(sets, customers):
    """Check if sets are less than or equal to customers."""
    try:
        return int(sets) <= int(customers)
    except ValueError:
        return False

def validate_total_amounts(cash_total, card_total, usd_total, total_price):
    """Check if the sum of cash, card, and USD totals equals the total price."""
    try:
        total = float(cash_total) + float(card_total) + float(usd_total)
        return abs(total - float(total_price)) < 0.01  # Allow for minor floating-point errors
    except ValueError:
        return False
