from flask import Flask, send_from_directory
from flask import jsonify
from src.api.utils.database import db, ma
from src.api.utils.responses import response_with
import src.api.utils.responses as resp
import logging
from os.path import join, dirname, realpath
from src.api.routes.voice_routes import voice_routes
from src.api.routes.voice_routes_v2 import voice_routes_v2
from src.api.routes.file_routes import file_routes
from src.api.config.config import ModelConfig as mc

app = Flask(__name__)
UPLOAD_FOLDER = join(dirname(realpath(__file__)), 'static/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
print(UPLOAD_FOLDER)

db.init_app(app)
ma.init_app(app)

with app.app_context():
    db.create_all()

app.register_blueprint(voice_routes_v2, url_prefix='/api/v2')
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

@app.route('/src/static/<path:path>')
def serve_page(path):
    return send_from_directory('/src/static', path, as_attachment=True)


with app.app_context():
    db.create_all()






