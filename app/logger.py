import logging
from logging.handlers import RotatingFileHandler
import os

def setup_logging():
    log_directory = "logs"
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)
    log_file_path = os.path.join(log_directory, 'app.log')

    # ロガーの設定
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # ファイルハンドラーの設定
    file_handler = RotatingFileHandler(log_file_path, maxBytes=1024*1024*5, backupCount=5, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

    # ルートロガーにハンドラーを追加
    logging.getLogger('').addHandler(file_handler)