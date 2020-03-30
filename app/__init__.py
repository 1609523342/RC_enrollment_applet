from flask import Flask
from app.models.Base_model import db


def creat_app():
    app = Flask(__name__)
    app.config.from_object('app.config')
    register_blueprint(app)
    db.init_app(app)
    db.create_all(app=app)
    return app


def register_blueprint(app):
    from app.MinA import MinAs
    app.register_blueprint(MinAs)


