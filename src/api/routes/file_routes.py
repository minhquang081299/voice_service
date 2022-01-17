from flask import Blueprint
from flask import request
from src.api.config.config import ModelConfig as mc
from src.api.config.config import Config as cf
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import os 
from pathlib import Path
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
    """this api accept file with duration of equal or bellow 16s

    Returns:
        response: contain data and error
    """
    error = None
    data = None
    payload = {}
    
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
            os.mkdir(f_pre)
            
        fp = os.path.join(f_pre, filename)
        file.save(fp)
        f_service = FileService(f_pre, filename)
        fnn = f_service.convert_audio()   
        #check suitable file
        if fnn!="":
            fp = os.path.join(f_pre, fnn)
            host =  request.host_url
            url = host+ f'static/data/{str(user)}/{fnn}'
            payload = {"url": url}
            data = DataModel(True, "FILE'S UPLOADED SUCCESSFULLY", payload)
            data = vars(data)
            response = ResponseModel(data, {})
            
        else:
            mess_err="Invalid or Missing Parameters. Check the duration and type of your audios. This version supports"\
                "audios are bellow 16 seconds with 'wav, mp3' extensions"
            error = ErrorModel("422", mess_err)
            error = vars(error)
            response = ResponseModel({}, error)
    
    else:
        error = ErrorModel("422", "Invalid or Missing Parameters. Not a wav or mp3 file")
        error = vars(error)
        response = ResponseModel({}, error)
        
    return json.dumps(vars(response))

