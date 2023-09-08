from flask import Blueprint, render_template,request, redirect, url_for, session,make_response, jsonify
from db.account_db import login
from db.account_db import select_userid
from datetime import timedelta
from .syntax_check import validate_password
from db.account_db import change_password
import string, random

login_bp = Blueprint('login', __name__, url_prefix='/login',
                      template_folder='templates',
                        static_url_path='/static',
                          static_folder='./static')

login_bp.secret_key = ''.join(random.choices(string.ascii_letters, k=256))


@login_bp.route('/',methods=['GET'])
def index():
    msg = request.args.get('msg')
    if msg != None:
        return render_template('index.html',msg=msg)
    else:
        return render_template('index.html')
    
    
@login_bp.route('/login_result')
def login_result():
    return render_template('result.html')
    
@login_bp.route('/login',methods=['POST'])
def login_function():
    mail=request.form.get('mail')
    pas = request.form.get('password')


    if login(mail,pas):
        ID = select_userid(mail)
        session['login_ID'] = str(ID[0])  # 整数を文字列に変換する
        session.permanent = True
        login_bp.permanent_session_lifetime = timedelta(minutes=5) 

        response = make_response("Cookie set successfully")
        response.set_cookie('session_cookie', value=session['login_ID'], httponly=True)
        return redirect(url_for('img.list',page_num=1)) 
    
    else:
        msg = "パスワードまたはメールアドレスが違います"
        input_data = {'mail':mail, 'pas':pas}
        return redirect(url_for('login.index',msg=msg, data=input_data)) 

    
@login_bp.route('/cahnge_pass',methods=['GET'])
def cahnge_pas():
    err = request.args.get('err')
    if err != None:
        return render_template('cahng_pass.html',err=err)
    else:
        return render_template('cahng_pass.html')
    

@login_bp.route('password_cahnge',methods=['POST'])
def password_cahnge():
    mail = request.form.get('mail')
    pas = request.form.get('password')
    
    if validate_password(pas) == False:
          err = "パスワードの形式が間違っています"
          return redirect(url_for('login.cahnge_pas',err=err))
      
    count = change_password(mail,pas)
    if count == 1:
        msg = 'パスワード変更が完了しました'
        return redirect(url_for('login.index',msg=msg))
    else:
        err = 'アカウントが見つかりません'
        return redirect(url_for('login.cahnge_pas',err=err))
        
    
@login_bp.route('/logout')
def logout():
    session.pop('user_name', None) 
    return redirect(url_for('index'))