from flask import request
from flask_restless import APIManager, ProcessingException
from app import create_app
from .models import Enzyme, Experiment, Method, db


access_password = 'mysecretkey'


def check_credentials(**kwargs):
    if request.headers.get('X-Secret-Key', '') != access_password:
        raise ProcessingException(code=401)  # Unauthorized


manager = APIManager(create_app(), flask_sqlalchemy_db=db)
# default endpoint: 127.0.0.1:8080/api/experiment
http_methods = ['GET', 'POST', 'PUT', 'DELETE']
protected = ['GET_SINGLE', 'POST', 'PUT_SINGLE', 'DELETE_SINGLE']
manager.create_api(Enzyme, methods=http_methods, preprocessors={a: [check_credentials] for a in protected})
manager.create_api(Method, methods=http_methods, preprocessors={a: [check_credentials] for a in protected})
manager.create_api(Experiment, methods=http_methods, preprocessors={a: [check_credentials] for a in protected})



