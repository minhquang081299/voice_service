import pathlib
from flask import request
from flask_sqlalchemy.model import Model
class Config(object):
    HOST = "0.0.0.0"
    PORT = 5000
    DEBUG = False
    TESTING = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
class ModelConfig(object):
    _ROOT = str(pathlib.Path(__file__).parent.parent.parent)
    W2V2_LM_PREFIX = _ROOT + '/static/model/LM/vi_lm_4grams.bin'
    W2V2_FOR_CTC_PREFIX = _ROOT + '/static/model/Wav2Vec2ForCTC'
    W2V2_PROCESSOR_PREFIX = _ROOT+ '/static/model/Wav2Vec2Processor'
    

    
class AudioConfig(object):
    EXTENSION = 'wav'
    SR = 16000
    MAX_DURATION = 30
    
