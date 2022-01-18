from flask import Blueprint
from flask import request
from src.api.model.response_model import ResponseModel, DataModel, ErrorModel
import src.api.utils.responses as resp
from src.api.services.voice_service import VoiceService
from src.api.config.config import ModelConfig as mc
from flask import Flask, flash, request, redirect, url_for
from src.api.services.file_service import FileService
from flask import Response, jsonify
from pathlib import Path
import os
from werkzeug.utils import secure_filename


voice_routes = Blueprint('voice_routes', __name__)

voice_service = VoiceService(mc.W2V2_LM_PREFIX,
                             mc.W2V2_PROCESSOR_PREFIX,
                             mc.W2V2_FOR_CTC_PREFIX)
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           
           
#v1: absoluted path for audio file
#v2: get url stream
@voice_routes.route('/voice-service/<int:user>', methods=['POST'])
def voice_regconition_controller(user):
    """this api accept file with duration of equal or bellow 25s
    Returns:
        response: contain data and error
    """
    error = None
    data = None
    payload = None
    rm = None
    
    #check conditions when receive a request from a client
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    #if there is a file requested to upload that's sastified
    
    if file and _allowed_file(file.filename):
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
            audio_path = os.path.join(f_pre, fnn)            
            rs = voice_service.voice_service(audio_path)
            payload = {'text': rs}
            data = DataModel(True, "Success", payload)
            data = vars(data)
            rm = ResponseModel(data,{})
        else:
            mess_err="Invalid or Missing Parameters. Check the duration and type of your audios. This version supports"\
                " audios are bellow 25 seconds with 'wav, mp3, m4a' extensions"
            error = ErrorModel("422", mess_err)
            error = vars(error)
            rm = ResponseModel({},error)
    else:
        error = ErrorModel("422", "Invalid or Missing Parameters. Not a wav, mp3 or m4a file")
        error = vars(error)
        rm = ResponseModel({},error)
        
    rm = jsonify(vars(rm)) 
    rm.headers["Content-Type"] = "application/json;charset=utf8"
    return rm

#v2: split_file
@voice_routes.route('/voice-service/long-audio/<int:user>', methods=['POST'])
def voice_regconition_controller_long_file(user):
    """this api accept file with duration of equal or bellow 25s
    Returns:
        response: contain data and error
    """
    error = None
    data = None
    payload = None
    rm = None
    
    #check conditions when receive a request from a client
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    
    #if there is a file requested to upload that's sastified
    
    if file and _allowed_file(file.filename):
        filename = secure_filename(file.filename)
       
        f_pre = str(Path(__file__).parent.parent.parent)+ f'/static/data/{str(user)}'
        
        if not os.path.exists(os.path.join(f_pre)):
            os.mkdir(f_pre)
            
        fp = os.path.join(f_pre, filename)
        file.save(fp)
        f_service = FileService(f_pre, filename)
        fnn = f_service.convert_long_audio()   
        
        #check suitable file
        if fnn!="":
            audio_path = os.path.join(f_pre, fnn)            
            rs = voice_service.long_voice_service(audio_path)
            rs = ' '.join(rs)
            payload = {'text': rs}
            data = DataModel(True, "Success", payload)
            data = vars(data)
            rm = ResponseModel(data,{})
        else:
            mess_err="Invalid or Missing Parameters. Check the type of your audios. This version supports"\
                " audios are bellow 25 seconds with 'wav, mp3, m4a' extensions"
            error = ErrorModel("422", mess_err)
            error = vars(error)
            rm = ResponseModel({},error)
    else:
        error = ErrorModel("422", "Invalid or Missing Parameters. Not a wav, mp3 or m4a file")
        error = vars(error)
        rm = ResponseModel({},error)
        
    rm = jsonify(vars(rm)) 
    rm.headers["Content-Type"] = "application/json;charset=utf8"
    return rm


