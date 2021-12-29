import pathlib

from flask_sqlalchemy.model import Model

class Config(object):
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ModelConfig(object):
    _ROOT = "/media/hoangnv/windata/company/project/apistt/src"
    W2V2_LM_PREFIX =_ROOT + '/static/model/LM/vi_lm_4grams.bin'
    W2V2_FOR_CTC_PREFIX = _ROOT+ '/static/model/Wav2Vec2ForCTC'
    W2V2_PROCESSOR_PREFIX = _ROOT+ '/static/model/Wav2Vec2Processor'
    UPLOAD_FOLDER = _ROOT+'/static/data/client'
