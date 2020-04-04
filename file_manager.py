import mimetypes
import os
from flask import jsonify

class FileManager:
    @staticmethod
    def manage_file(file_name):
        file_manager = get_file_manager(file_name)
        return file_manager


def get_file_manager(file_name):
    try:
        file_type = mimetypes.MimeTypes().guess_type(file_name)[0]
    except FileNotFoundError as ex:
        return jsonify(ex.strerror)

    if file_type is not None:
        if 'text' in file_type:
            return manage_text_file(file_name)
        elif 'application' in file_type:
            return manage_application_file(file_name)
        else:
            return manage_other_file(file_name)
    else:
        return jsonify("Can't recognize file type")

def manage_text_file(file_name):
    try:
        with open(file_name, 'r') as f:
            data = f.read()
            return jsonify(data)
    except FileNotFoundError as ex:
        return jsonify(ex.strerror)

def manage_application_file(file_name):
    try:
        result = os.system(file_name)
        return jsonify(result)
    except BaseException as ex:
        return jsonify(ex.strerror)

def manage_other_file(file_name):
    return jsonify(file_name)

