from smtplib import SMTP
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os,email.utils

def send_mail(mail,token):
    ID = 'h.kikuchi.sys22@morijyobi.ac.jp'
    PASS = os.environ['MAIL_PASS']
    HOST = 'smtp.gmail.com'
    PORT = 587
    
    
    msg = MIMEMultipart()
    
    text = f'下記のURLにアクセスしてアカウント登録を完了させてください \n URL : http://127.0.0.1:5000/user/confirm_email/{token}'
    
    subject = 'ユーザー登録のお知らせ'
        
    
    msg.attach(MIMEText(text, 'html'))
    
    msg['Subject'] = subject
    msg['From'] = email.utils.formataddr(('システムメール', ID))
    msg['To'] = email.utils.formataddr(('ユーザ様', mail))
    
    server = SMTP(HOST, PORT)
    server.starttls()

    server.login(ID, PASS)  # ログイン認証

    server.send_message(msg)  # 送信！！！

    server.quit()   # サーバ切断