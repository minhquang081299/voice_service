from flask import Blueprint
from flask import request
from src.api.config.config import ModelConfig as mc
from src.api.config.config import Config as cf
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os 
from pathlib import Path
from os.path import join, dirname, realpath
from src.api.model.response_model import ResponseModel, DataModel, ErrorModel
from flask import Response, jsonify
import json
from src.api.utils.responses import response_with
from src.api.services.file_service import FileService


ALLOWED_EXTENSIONS = {'wav', 'mp3'}
file_routes = Blueprint('file_routes', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

@file_routes.route('/upload-short-audio-file/<int:user>', methods=['POST'])
def upload_short_audio_file(user):
    """this api accept file with duration of equal or above 16s with sample rate 16khz

    Returns:
        response: contain data and error
    """
    error = None
    data = None
    payload = {}
    fp_uri = None
    
    #check condition when receive a request from a client
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    #if there is a file requested to upload that's sastified
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
       
        f_pre = str(Path(__file__).parent.parent.parent)+ f'/static/data/{str(user)}'
        
        if not os.path.exists(os.path.join(f_pre)):
            print(os.getcwd())
            os.mkdir(f_pre)
            
        fp = os.path.join(f_pre, filename)
        file.save(fp)
        
        f_service = FileService(f_pre, filename)
        fnn = f_service.convert_audio()
        
        
        fp = os.path.join(f_pre, fnn)
        payload = {"url": fp}

        data = DataModel(True, "FILE'S UPLOADED SUCCESSFULLY", payload)
        data = vars(data)
        response = ResponseModel(data, {})
        return json.dumps(vars(response))
    
    else:
        error = ErrorModel("422", "Invalid or Missing Parameters")
        error = vars(error)
        response = ResponseModel({}, error)
        return json.dumps(vars(response))

