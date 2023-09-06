from flask import Blueprint, render_template,request, redirect, url_for, session
from db.account_db import inset_ad_user
from datetime import timedelta

user_bp = Blueprint('user', __name__, url_prefix='/user',
                      template_folder='templates',
                        static_url_path='/static',
                          static_folder='./static')

@user_bp.route('/register')
def register():
     return render_template('register.html')

@user_bp.route('/result')
def result():
     return render_template('index.html')

@user_bp.route('/register_exe', methods=['POST'])
def register_account():
    mail = request.form.get('mail')
    pas = request.form.get('pas')
    
    count = inset_ad_user(mail,pas)
    if count == 1:
        #   mail.mail(user,mailad,type,pas)
          return redirect(url_for('user.result'))
    else:
         return redirect(url_for('user.result'))
    