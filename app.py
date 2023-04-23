import os
from flask import Flask, flash, request, redirect, render_template, \
    url_for
from werkzeug.utils import secure_filename
# from flask_dropzone import Dropzone
import connection_secret
import file_manager as fm

app = Flask(__name__,
            template_folder="templates")
app.config.from_pyfile('config.py')

app.secret_key = connection_secret.secret_key

# dropzone = Dropzone(app)

AFM = fm.AzureBlobManager(conn_str=connection_secret.conn_str,
                          container_name=app.config['AZURE_STORAGE_CONTAINER'])


@app.route('/')
def index():
    files = AFM.listBlobs()
    size = '{0:.3f} MB'.format(AFM.containerSize()/1e6)
    return render_template('layout_static.html', files=files, size=size)


@app.route('/', methods=['POST'])
def upload_file():

    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        # if no name
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)

        # if success
        if file and fm.allowedFileExtension(file.filename,
                                            app.config['UPLOAD_EXTENSIONS']):
            filename = secure_filename(file.filename)

            AFM.upload(flsk_file=file)

            flash('File successfully uploaded')

            return redirect(url_for('index'))

        else:
            flash('Allowed file types are txt, pdf, png, jpg, jpeg, gif')
            return redirect(request.url)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)
