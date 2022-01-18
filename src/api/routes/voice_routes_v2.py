from threading import local
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
import requests
from werkzeug.utils import secure_filename

voice_routes_v2 = Blueprint('voice_routes_v2', __name__)

voice_service = VoiceService(mc.W2V2_LM_PREFIX,
                             mc.W2V2_PROCESSOR_PREFIX,
                             mc.W2V2_FOR_CTC_PREFIX)
ALLOWED_EXTENSIONS = {'wav', 'mp3', 'm4a'}

def _allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def download_file(url, output_prefix):
    local_filename = url.split('/')[-1]
    local_filename = secure_filename(local_filename)
    output_prefix = output_prefix+'/'+local_filename
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(output_prefix, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192): 
                f.write(chunk)
    return output_prefix
           
#v1: absoluted path for audio file


#v2: split_file
@voice_routes_v2.route('/voice-service/<int:user>', methods=['POST'])
def voice_regconition_controller_long_file(user):
    """taccept long files
    """
    error = None
    data = None
    payload = None
    rm = None
    
    #check conditions when receive a request from a client
    rfc = request.get_json()
    url = rfc['url']
    downloaded_file_path = ""
    
        
    #if there is a file requested to upload that's sastified
    
    f_pre = str(Path(__file__).parent.parent.parent)+ f'/static/data/{str(user)}'
    
    if not os.path.exists(os.path.join(f_pre)):
        os.mkdir(f_pre)
    try:
        downloaded_file_path=download_file(url, f_pre)
        
    except Exception as e:
        print(e)
        mess_err="Cannot download file, maybe missing parameter or your links's not available"
        error = ErrorModel("422", mess_err)
        error = vars(error)
        rm = ResponseModel({},error)
        return rm
    
    filename = downloaded_file_path.split('/')[-1]
    
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
    
        
    rm = jsonify(vars(rm)) 
    rm.headers["Content-Type"] = "application/json;charset=utf8"
    return rm
