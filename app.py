from flask import Flask, render_template, request, send_file
from werkzeug.utils import secure_filename
import os
from main import change_pitch

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads/'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        file = request.files['file']
        sem = int(request.form.get('select'))
        print(file, sem, type(sem))
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            converted_path = change_pitch(os.path.join(app.config['UPLOAD_FOLDER'], filename), './out', sem)
            converted_name = os.path.basename(converted_path)
            return send_file(converted_path, as_attachment=True, download_name=converted_name)
    return render_template('index.html')
