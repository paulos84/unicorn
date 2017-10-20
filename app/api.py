from app.models import Experiment, Enzyme, Reactants, Conditions, db
from flask_restless import APIManager
from app import create_app


manager = APIManager(create_app(), flask_sqlalchemy_db=db)

manager.create_api(Experiment, methods=['GET', 'POST', 'DELETE'])

