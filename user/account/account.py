from flask import Blueprint, render_template, redirect, url_for
from flask import request, session
from db.account_db import inset_ad_user
from datetime import timedelta
from .syntax_check import syntax_check
from .syntax_check import validate_password
from .token_generator import generate_token
from .mail import send_mail

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


@user_bp.route('/stand')
def stand():
    return render_template('stand.html')


@user_bp.route('/register_exe', methods=['POST'])
def register_account():
    mail = request.form.get('mail')
    pas = request.form.get('password')
    if validate_password(pas) is False:
        err = "パスワードの形式が間違っています"
        return redirect(url_for('user.result', err=err))
    token = generate_token()
    session['token'] = token
    print(session['token'])
    session['mail'] = mail
    session['pas'] = pas
    session.permanent = True
    user_bp.permanent_session_lifetime = timedelta(minutes=5)

    send_mail(mail, token)

    return redirect(url_for('user.stand'))


@user_bp.route('/confirm/<token>', methods=['GET'])
def confirm_email(token):
    err = None
    msg = None

    if not token:
        err = "メールを入力しアカウント登録を完了させてください"
    else:
        TOKEN = session.get('token')
        print(f'TOKEN: {TOKEN} : token: {token}')
        if TOKEN != token:
            err = "トークンが無効です"
        else:
            mail = session.get('mail')
            pas = session.get('pas')

            if syntax_check(mail):
                count = inset_ad_user(mail, pas)
                if count == 1:
                    msg = '登録が完了しました'
                else:
                    msg = '登録に失敗しました'
            else:
                err = 'メールアドレスが有効ではありません'

    session.pop('token', None)

    if err:
        return redirect(url_for('user.result', err=err))
    elif msg:
        return redirect(url_for('user.result', msg=msg))
    else:
        return redirect(url_for('user.result'))

@user_bp.route('/generate')
def generate():
    return render_template('generate.html')
