from flask import Flask, render_template, flash, redirect, request, url_for
import os
from werkzeug.utils import secure_filename
import glob
from sudoku_solver import *

default_file_name = 'test'
app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads/'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def allowed_file_ext(filename):
    return filename.rsplit('.', 1)[1].lower()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['POST'])
def upload_image():
    files = glob.glob(UPLOAD_FOLDER + "*")
    for f in files:
        os.remove(f)

    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        temp_name = default_file_name + "." + allowed_file_ext(filename)
        os.rename((os.path.join(UPLOAD_FOLDER, filename)), (os.path.join(UPLOAD_FOLDER, temp_name)))
        # print('upload_image filename: ' + filename)
        flash('Image successfully uploaded, Please wait')
        execute(allowed_file_ext(filename))
        return render_template('index.html', filename=temp_name)
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route('/display/<filename>')
def display_image(filename):
    # print('display_image filename: ' + filename)
    return redirect(url_for('static', filename='uploads/' + filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)
