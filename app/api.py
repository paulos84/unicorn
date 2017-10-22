from app.models import Experiment, Enzyme, Reactants, Conditions, db
from flask_restless import APIManager
from app import create_app
from flask import Blueprint


experiment = Blueprint('experiment', __name__)

@experiment.route('/')
def hourly_data_1(pollutant, name):
    return 'test'




