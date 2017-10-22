from app.models import Experiment, Enzyme, Reactants, Conditions, db
from flask import Blueprint


experiment = Blueprint('experiment', __name__)

@experiment.route('/')
def hourly_data_1():
    pass




