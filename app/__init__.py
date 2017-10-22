from flask import Flask
from app.models import db
from flask_restless import APIManager

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.DevelopmentConfig')
    from .api import experiment
    app.register_blueprint(experiment)
    db.init_app(app)
    with app.app_context():
        return app


def create_test_app():
    app = Flask(__name__)
    app.config.from_object('config.TestingConfig')
    db.init_app(app)
    app.app_context().push()
    return app

