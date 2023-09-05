from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/generate')
def generate():
    return render_template('generate.html')

@app.route('/upload', methods=['POST'])
def upload_file():    
    if 'file' not in request.files:
        return jsonify({'message': 'No file part'})

    file = request.files['file']
    
    if file.filename == '':
        return jsonify({'message': 'No selected file'})

    # ファイルを保存、または処理するコードをここに追加
    # 例: file.save('uploads/' + secure_filename(file.filename))
    
    
    
    
    
    
    return jsonify({'message': 'File uploaded successfully'})

if __name__ == '__main__':
    app.run(debug=True)