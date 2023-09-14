from flask import Blueprint, render_template, redirect, url_for, make_response
from flask import request, session
from db.account_db import ad_login
from db.account_db import select_userid
from datetime import timedelta
from user.account.token_generator import generate_token
from user.account.mail import send_ad_mail_pass
from user.account.syntax_check import syntax_check
from user.account.syntax_check import validate_password
from db.account_db import change_ad_password
import string
import random

admin_bp = Blueprint('admin', __name__, url_prefix='/admin',
                     template_folder='templates',
                     static_url_path='/static',
                     static_folder='./static')

admin_bp.secret_key = ''.join(random.choices(string.ascii_letters, k=256))


@admin_bp.route('/admin', methods=['GET'])
def admin():
    data = request.args.get('data')
    msg = request.args.get('msg')
    if msg is not None:
        return render_template('admin.html', msg=msg, data=data)
    else:
        return render_template('admin.html')


@admin_bp.route('/login_result')
def login_result():
    return render_template('result.html')


@admin_bp.route('/login', methods=['POST'])
def login_function():
    mail = request.form.get('mail')
    pas = request.form.get('pas')

    if ad_login(mail, pas):
        ID = select_userid(mail)
        session['login_ID'] = str(ID[0])
        session.permanent = True
        admin_bp.permanent_session_lifetime = timedelta(minutes=5)
        response = make_response("Cookie set successfully")
        response.set_cookie(
            'session_cookie', value=session['login_ID'], httponly=True)
        return redirect(url_for('list.ac_list', page_num=1, type=type))

    else:
        msg = "パスワードまたはメールアドレスが違います"
        input_data = {'mail': mail, 'pas': pas}
        return redirect(url_for('admin.admin', msg=msg, data=input_data))


@admin_bp.route('/cahnge_pass', methods=['GET'])
def cahnge_pas():
    err = request.args.get('err')
    if err is not None:
        return render_template('change_adpss.html', err=err)
    else:
        return render_template('change_adpss.html')


@admin_bp.route('password_cahnge', methods=['POST'])
def password_cahnge():
    mail = request.form.get('mail')
    pas = request.form.get('password')

    if validate_password(pas) is False:
        err = "パスワードの形式が間違っています"
        return redirect(url_for('login.cahnge_pas', err=err))
    token = generate_token()
    session['token'] = token
    print(session['token'])
    session['mail'] = mail
    session['pas'] = pas
    session.permanent = True
    admin_bp.permanent_session_lifetime = timedelta(minutes=5)

    send_ad_mail_pass(mail, token)
    return render_template('stand.html')


@admin_bp.route('/pass_change/<token>',methods=['GET'])
def pass_change(token):
    err = None
    msg = None
    if not token:
        err = "メールを登録して完了させてください"
    else:
        TOKEN = session.get('token')
        print(f'TOKEN: {TOKEN} : token: {token}')
        if TOKEN != token:
            err = "トークンが無効です"
        else:
            mail = session.get('mail')
            pas = session.get('pas')

            if syntax_check(mail):
                count = change_ad_password(mail, pas)
                if count == 1:
                    msg = 'パスワード変更が完了しました'
                else:
                    err = 'パスワード変更に失敗しました'
            else:
                err = 'メールアドレスが有効ではありません'

    session.pop('token', None)
    if err:
        return redirect(url_for('admin.cahnge_pas', err=err))
    elif msg:
        return redirect(url_for('admin.admin',msg = msg))
@admin_bp.route('/logout')
def logout():
    session.pop('user_name', None)
    return redirect(url_for('index'))
