import smtplib
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os
from flask import current_app
import ast
def send_email_with_form_data(form_data):
    """フォームデータをCSV形式でメールで送信する関数"""

    # 環境変数のロード
    load_dotenv()

    # SMTP設定を環境変数から取得
    smtp_server = os.getenv('SMTP_SERVER')
    smtp_port = int(os.getenv('SMTP_PORT'))
    outlook_email = os.getenv('OUTLOOK_EMAIL')
    outlook_password = os.getenv('OUTLOOK_PASSWORD')
    # ヘッダーを追加
    headers = ['日付', '組数', '客数', '丼数', '仕入れ額', '合計値段', '現金合計', 'カード合計', 'USD負担合計', '備考欄']
    # CSV形式の文字列を作成
    email_body = ",".join(headers) + "\n"

    # フォームデータの値を取得してCSV形式の文字列に変換
    csv_data = ",".join([str(form_data.get(header, '')) for header in [
        'date', 'sets', 'customers', 'bowls', 'purchase_total',
        'total_price', 'cash_total', 'card_total', 'usd_total', 'remarks'
    ]])

    email_body += csv_data
    
    email_list_str = os.getenv('EMAIL_LIST')
    print(email_list_str)
    email_list = ast.literal_eval(email_list_str) if email_list_str else []
    recipients = email_list  
    print(email_list, 'email_listです。')
    to_addresses = ", ".join(recipients)
    print(to_addresses, "to_addressです。")
    # MIMETextオブジェクトを作成し、メールの本文、件名、送信元、宛先を設定
    msg = MIMEText(email_body, 'plain', 'utf-8')
    msg['Subject'] = f"{form_data['date']} 売上集計"
    msg['From'] = outlook_email
    msg['To'] = to_addresses

    try:
        # SMTPサーバーに接続し、メールを送信
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.set_debuglevel(1)
            server.ehlo()
            server.starttls()
            server.login(outlook_email, outlook_password)
            server.sendmail(outlook_email, to_addresses, msg.as_string())
        print("Email sent successfully")
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False