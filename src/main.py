import os
from flask import Flask, send_from_directory
from flask import jsonify
from api.utils.database import db, ma
from api.utils.responses import response_with
import api.utils.responses as resp
import logging
from api.routes.voice_routes import voice_routes
from api.routes.file_routes import file_routes
from api.config.config import ModelConfig as mc
app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = mc.UPLOAD_FOLDER
db.init_app(app)
ma.init_app(app)
with app.app_context():
    db.create_all()


app.register_blueprint(voice_routes, url_prefix='/api/v1')
app.register_blueprint(file_routes, url_prefix='/api/v1/files')

@app.after_request
def add_header(response):
    return response


@app.errorhandler(400)
def bad_request(e):
    logging.error(e)
    return response_with(resp.BAD_REQUEST_400)


@app.errorhandler(500)
def server_error(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_500)


@app.errorhandler(404)
def not_found(e):
    logging.error(e)
    return response_with(resp.SERVER_ERROR_404)


db.init_app(app)
ma.init_app(app)



with app.app_context():
    db.create_all()






