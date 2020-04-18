from flask import Flask
from app.models.Base_model import db
from flask_cors import *


#往flask注册插件
def creat_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    register_blueprint(app)
    db.init_app(app)
    db.create_all(app=app)
    CORS(app, supports_credentials=True)
    return app


def register_blueprint(app):
    from app.MinA import MinAs
    app.register_blueprint(MinAs)


