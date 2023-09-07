import os
from flask import Flask , render_template, request, url_for,session
from flask_session import Session
import secrets
from user.account.account import user_bp
from user.account.login import login_bp
from admin.adminuser.adminlogin import admin_bp
from admin.account_list.list import list_bp
import string, random


app = Flask(__name__)
secret_key = secrets.token_hex(16)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))
app.register_blueprint(user_bp)
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(list_bp)

app.config['SESSION_TYPE'] = 'filesystem'  
app.config['SESSION_PERMANENT'] = False  
app.config['SESSION_USE_SIGNER'] = True  
app.config['SECRET_KEY'] = secret_key

Session(app)
#ログイン画面

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)