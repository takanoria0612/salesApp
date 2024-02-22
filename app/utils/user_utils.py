import os
import json
from typing import Dict

def load_user_from_env() -> Dict[str, Dict]:
    users_json = os.getenv('USERS_JSON', '{}')  # 環境変数からJSON形式の文字列を取得
    user_database = json.loads(users_json)  # JSON形式の文字列をPythonの辞書に変換
    return user_database
