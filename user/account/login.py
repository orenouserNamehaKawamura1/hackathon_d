from flask import Blueprint, render_template,request, redirect, url_for, session,make_response, jsonify
from db.account_db import login
from db.account_db import select_userid
from datetime import timedelta
import string, random

login_bp = Blueprint('login', __name__, url_prefix='/login',
                      template_folder='templates',
                        static_url_path='/static',
                          static_folder='./static')

login_bp.secret_key = ''.join(random.choices(string.ascii_letters, k=256))


@login_bp.route('/',methods=['GET'])
def index():
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
        # response = make_response(redirect(url_for('login.login_result', type=type)))
        # response.set_cookie('session_cookie', value=session['login_ID'], httponly=True)

        return redirect(url_for('img.list',page_num=1)) 
            
    else:

        return jsonify({'success': False, 'message': 'ユーザー名またはパスワードが正しくありません'})

    

@login_bp.route('/logout')
def logout():
    session.pop('user_name', None) 
    return redirect(url_for('index'))