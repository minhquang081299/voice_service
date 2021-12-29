from flask import Blueprint
from flask import request
from api.utils.responses import response_with
from api.config.config import ModelConfig as mc
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os 

file_routes = Blueprint('file_routes', __name__)

from flask import Response, jsonify

# UPLOAD_FOLDER = './static/data/client'
ALLOWED_EXTENSIONS = {'wav', 'mp3'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
# @file_routes.route('/upload_file', methods=['GET', 'POST'])
# def upload_file():
#     data = request.get_json()
#     audio_path = data["file"]
#     print(audio_path)
   
#     rs = file_routes.voice_service(audio_path)
#     resp = jsonify(rs)
#     resp.headers["Content-Type"] = "application/octet-stream"
#     return resp

@file_routes.route('/upload-file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        print(request)
        # check if the post request has the file part
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(mc.UPLOAD_FOLDER, filename))
            return ""
