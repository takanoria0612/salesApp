import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))

class Config(object):
    SECRET_KEY = os.getenv('SECRET_KEY')
    SMTP_SERVER = os.getenv('SMTP_SERVER')
    SMTP_PORT = int(os.getenv('SMTP_PORT'))
    OUTLOOK_EMAIL = os.getenv('EMAIL_LIST')
    OUTLOOK_PASSWORD = os.getenv('OUTLOOK_PASSWORD')
    USER_COUNT = int(os.getenv('USER_COUNT', 0))
    USER_NAME = os.getenv('USER_NAME')
    USER_PASSWORD = os.getenv('USER_PASSWORD')
    EXCEL_FILE_PATH = os.getenv('EXCEL_FILE_PATH')
    OUTLOOK_EMAIL= os.getenv('OUTLOOK_EMAIL')