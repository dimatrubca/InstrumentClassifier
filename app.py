import os
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
from flask import send_from_directory
import PIL
import torchvision.transforms as T
from fastai.vision import *
import numpy as np
import time

def load_model():
    return load_learner('models', 'export.pkl')

UPLOAD_FOLDER = 'C:/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
trained_model = load_model()


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        print(request.method)
        # check if the post request has the file part
        if 'upload-image' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['upload-image']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print(type(file))
            img_pil = PIL.Image.open(file.stream)
            img_tensor = T.ToTensor()(img_pil)
            # img_fastai = Image(img_tensor)
            img_fastai = open_image(file.stream)

            _, _, preds = trained_model.predict(img_fastai)
            print(trained_model.predict(img_fastai))
            print(trained_model.data.classes)
            idx = np.argmax(preds) # preds are log probabilities of classes
            category = trained_model.data.classes[idx]

            print(img_pil.size)
            print("!!!")
            file.seek(0)
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            return category
            # return redirect("/", category=category)
            # return redirect(url_for('uploaded_file',
            #                         filename=filename))

    return render_template('index.html')
    # '''
    # <!doctype html>
    # <title>Upload new File</title>
    # <h1>Upload new File</h1>
    # <form method=post enctype=multipart/form-data>
    #   <input type=file name=file>
    #   <input type=submit value=Upload>
    # </form>
    # '''


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)


if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)