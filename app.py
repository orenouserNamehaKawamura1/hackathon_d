from flask import Flask , render_template, request, url_for
import db

app = Flask(__name__)

#ログイン画面
@app.route('')
def index():
    return render_template('index.html')

#アカウント登録
@app.route('/register')
def register():
    return render_template('register.html')

#画像生成画面
@app.route('/generate')
def generate():
    return render_template('generate.html')

#画像表示画面
@app.route('/preview')
def preview():
    return render_template('preview.html')

#利用者メニュー
@app.route('/user')
def user_menu():
    return render_template('user_menu.html')

#画像一覧
@app.route('/list')
def img_list():
    return render_template('list.html')

#画像詳細
@app.route('/detail')
def img_detail():
    return render_template('detail.html')

#画像削除確認画面
@app.route('/delete')
def img_delete():
    return render_template('delete.html')
