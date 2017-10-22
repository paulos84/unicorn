from app.models import Experiment, Enzyme, Reactants, Conditions, db
from flask import Blueprint,jsonify


experiment = Blueprint('experiment', __name__)

@experiment.route('/')
def experiment():
    return jsonify([a.aim for a in Experiment.query.first()])






