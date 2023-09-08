import os
from flask import Flask , render_template, request, url_for
import db
from user.account.account import user_bp
from user.account.login import login_bp
from user.img_lists.img_list import img_list_bp
from admin.adminuser.adminlogin import admin_bp
from admin.account_list.list import list_bp
import string, random


app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))
app.register_blueprint(user_bp)
app.register_blueprint(login_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(list_bp)
app.register_blueprint(img_list_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)