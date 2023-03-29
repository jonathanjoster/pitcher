from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from main import download, change_pitch

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form.get('url')
        file = request.files['file']
        sem = int(request.form.get('select'))
        print(f'url: {url}, file: {file}, sem: {sem}')
        if url is not None:
            audio_path = download(url, './out')
            converted_path = change_pitch(audio_path, './out', sem)
            converted_name = os.path.basename(converted_path)
            return send_file(converted_path, as_attachment=True, download_name=converted_name)
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            converted_path = change_pitch(os.path.join(app.config['UPLOAD_FOLDER'], filename), './out', sem)
            converted_name = os.path.basename(converted_path)
            return send_file(converted_path, as_attachment=True, download_name=converted_name)
    return render_template('index.html')
