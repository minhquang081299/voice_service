from flask import config
from main import app 
from api.config.config import Config as cf
if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(port=cf.PORT,
                    host=cf.HOST)