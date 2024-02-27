import logging
from flask import flash
from flask_login import UserMixin, LoginManager
from app.utils.user_utils import load_user_from_env

login_manager = LoginManager()

class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password


    @staticmethod
    def authenticate(username, password):
        logging.basicConfig(level=logging.DEBUG)
        user_database = load_user_from_env()
        print(username, password, 'def authenticate')
        logging.debug(f"Loaded user database: {user_database}")
        for user_id, user_data in user_database.items():
            if user_data['username'] == username:
                if user_data['password'] == password:
                    logging.debug(f"Authenticated user: {username}")
                    return User(user_data['id'], username, password)
                else:
                    flash("ユーザー名またはパスワードが間違っています", 'error')
                    logging.debug(f"Password mismatch for user: {username}")
                    return None

        flash("ユーザー名またはパスワードが間違っています", 'error')
        logging.debug(f"User not found: {username}")
        return None


    @staticmethod
    def get(user_id):
        user_database = load_user_from_env()
        for user_info in user_database.values():
            if user_info['id'] == user_id:
                return User(user_info['id'], user_info['username'], user_info['password'])
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

from datetime import datetime
from typing import Optional, Dict, Any

class ExcelDataRow:
    def __init__(self, date: datetime, sets: int, customers: int, bowls: int, 
                purchase_total: float, cash_total: float, card_total: float, 
                usd_total: float, total_price: float, remarks: str):
        self.date = date
        self.sets = sets
        self.customers = customers
        self.bowls = bowls
        self.purchase_total = purchase_total
        self.cash_total = cash_total
        self.card_total = card_total
        self.usd_total = usd_total
        self.total_price = total_price
        self.remarks = remarks

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        """
        Create an ExcelDataRow instance from a dictionary.
        Handles type conversion and defaults.
        """
        return cls(
            date=datetime.strptime(data.get('date', ''), '%Y-%m-%d').date(),
            sets=int(data.get('sets', 0)),
            customers=int(data.get('customers', 1)),
            bowls=int(data.get('bowls', 0)),
            purchase_total=float(data.get('purchase_total', 0.0)),
            cash_total=float(data.get('cash_total', 0.0)),
            card_total=float(data.get('card_total', 0.0)),
            usd_total=float(data.get('usd_total', 0.0)),
            total_price=float(data.get('total_price', 0.0)),
            remarks=data.get('remarks', ''),
        )

    def to_excel_row(self):
        """
        Convert the ExcelDataRow instance into a format suitable for Excel.
        """
        return [
            self.date,
            self.sets,
            self.customers,
            self.bowls,
            self.purchase_total,
            self.cash_total,
            self.card_total,
            self.usd_total,
            self.total_price,
            self.remarks,
        ]