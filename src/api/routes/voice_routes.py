from flask import Blueprint
from flask import request

import src.api.utils.responses as resp
from src.api.services.voice_service import VoiceService
from src.api.config.config import ModelConfig as mc
voice_routes = Blueprint('voice_routes', __name__)

from flask import Response, jsonify
voice_service = VoiceService(mc.W2V2_LM_PREFIX,
                             mc.W2V2_PROCESSOR_PREFIX,
                             mc.W2V2_FOR_CTC_PREFIX)

#v1: absoluted path for audio file
#v2: get url stream
@voice_routes.route('/voice-service', methods=['GET'])
def voice_regconition_controller():
    data = request.get_json()
    audio_path = data["file"]
    rs = voice_service.voice_service(audio_path)
    resp = jsonify(rs)
    resp.headers["Content-Type"] = "application/json;charset=utf8"
    return resp
