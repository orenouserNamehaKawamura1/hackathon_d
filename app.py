from flask import Flask , render_template
import string,random
from admin.list import list_bp

app = Flask(__name__)
app.secret_key = ''.join(random.choices(string.ascii_letters, k=256))
app.register_blueprint(list_bp)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
