# import os
# from typing import Dict

# def load_user_from_env() -> Dict[str, Dict]:
#     user_database = {}
#     user_count = int(os.getenv('USER_COUNT', 0))  # USER_COUNT 環境変数で管理されるユーザーの数
#     for i in range(1, user_count + 1):
#         username = os.getenv(f'USERNAME{i}')
#         password = os.getenv(f'PASSWORD{i}')
#         if username and password:
#             user_database[username] = {"id": str(i), "username": username, "password": password}
#     return user_database
import os
import json
from typing import Dict

def load_user_from_env() -> Dict[str, Dict]:
    users_json = os.getenv('USERS_JSON', '{}')  # 環境変数からJSON形式の文字列を取得
    user_database = json.loads(users_json)  # JSON形式の文字列をPythonの辞書に変換
    return user_database
