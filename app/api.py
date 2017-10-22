from app.models import Experiment, Enzyme, Reactants, Conditions, db
from flask import Blueprint,jsonify


experiment = Blueprint('experiment', __name__)

@experiment.route('/')
def experiment():
    exp = Experiment.query.first()
    return jsonify ('number'=exp.id)






