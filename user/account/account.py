from flask import Blueprint, render_template, redirect, url_for, make_response,jsonify
from flask import request, session
from db.account_db import inset_ad_user
from db.account_db import img_post
from datetime import timedelta
from .syntax_check import syntax_check
from .syntax_check import validate_password
from .token_generator import generate_token
from .mail import send_mail
import os
from datetime import datetime
from .AudioToImage import thread_func
import requests
from PIL import Image
from io import BytesIO
ALLOWED_EXTENSIONS = set(['mp3', 'wav', 'mp3'])

user_bp = Blueprint('user', __name__, url_prefix='/user',
                    template_folder='templates',
                    static_url_path='/static',
                    static_folder='./static')


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
def download_image(url):
    response = requests.get(url)
    if response.status_code == 200:
        return BytesIO(response.content)
    else:
        return None
def current_time_in_seconds():
    now = datetime.now()
    seconds_since_midnight = (now - now.replace(hour=0, minute=0, second=0, microsecond=0)).total_seconds()
    return int(seconds_since_midnight)

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


@user_bp.route('/generate', methods=['GET'])
def generate():
    return render_template('generate.html')


@user_bp.route('/generate', methods=['POST'])
def generate_post():
    id = session.get('login_ID')
    file = request.files['xhr2upload']
    if file and allowed_file(file.filename):
        filename = file.filename
        file.save(os.path.join('./temp/uploads', filename))

        url = thread_func(filename)
        image_data = download_image(url)
        if image_data:
            # 画像を開いて表示
            current_seconds = current_time_in_seconds()
            img = Image.open(image_data)
            img.show()
            # ローカルに保存するパス
            path = f"static/imge/{current_seconds}.png"
            img.save(path)
            # DBに保存するパス
            paths = f"imge/{current_seconds}.png"
            img_post(paths, id)
            data = 'ok'
            return jsonify(data)
        else:
            print("画像のダウンロードに失敗しました.")
