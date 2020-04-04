from flask import jsonify
from os import listdir
import mimetypes
from os.path import join, dirname, realpath, isfile
from pathlib import Path

import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename

app = Flask(__name__)

app.config.update(
    TESTING=True,
    SECRET_KEY=b'_5#y2L"F4Q8z\n\xec]/',
    UPLOAD_FOLDER=join(dirname(realpath(__file__)), 'static/')
)


@app.route('/files/', defaults={'file_name': None}, methods=['GET', 'DELETE'])
@app.route('/files/<file_name>', methods=['GET', 'DELETE'])
def list(file_name):
    if request.method == 'GET':
        if file_name is None:
            onlyfiles = [f for f in listdir(app.config['UPLOAD_FOLDER']) if
                         isfile(join(app.config['UPLOAD_FOLDER'], f))]
            return jsonify(onlyfiles)
        try:
            file_type = mimetypes.MimeTypes().guess_type(app.config['UPLOAD_FOLDER'] + file_name)[0]
            if file_type is not None:
                if 'text' in file_type:
                    with open(app.config['UPLOAD_FOLDER'] + file_name, 'r') as f:
                        data = f.read()
                        return jsonify(data)

                elif 'application' in file_type:
                    try:
                        result = os.system(app.config['UPLOAD_FOLDER'] + file_name)
                        return jsonify(result)
                    except BaseException as ex:
                        return jsonify(ex.strerror)
                # For all the others files return the path
                else:
                    file_url = app.config['UPLOAD_FOLDER'] + file_name
                    return jsonify(file_url)

            else:
                return jsonify("Can't recognize file type")
        except FileNotFoundError as ex:
            return jsonify(ex.strerror)

    elif request.method == 'DELETE':
        try:
            os.remove(app.config['UPLOAD_FOLDER'] + file_name)
            return redirect(url_for('list'))
        except FileNotFoundError as ex:
            return jsonify(ex.strerror)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(url_for('list'))
        file = request.files['file']
        if file.filename == '':
            return redirect(url_for('list'))
        if file:
            filename = secure_filename(file.filename)
            try:
                if 'overwrite' in request.form:
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                    return redirect(url_for('list'))
                else:
                    if Path(os.path.join(app.config['UPLOAD_FOLDER'], filename)).is_file():
                        error = "File with this name already exists"
                        return jsonify(error)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

            except Exception as ex:
                return jsonify(ex.strerror)
            return redirect(url_for('list'))

    return '''
        <!doctype html>
        <title>Add new File</title>
        <h1>Add new File</h1>
        <form method=post enctype=multipart/form-data>
          <input type=file name=file>
          <input type=submit value=Upload>
          <input type="checkbox" name="overwrite">
          <label for="checkbox">Overwrite</label>

        </form>
        '''


if __name__ == '__main__':
    app.run()
