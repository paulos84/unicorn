from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Enzyme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dose = db.Column(db.Float(50), nullable=False)
    experiments = db.relationship('Experiment', backref='owner_enzyme', lazy='dynamic')

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float(50), nullable=False)
    lactose = db.Column(db.Float(50), nullable=False)
    water = db.Column(db.Float(50), nullable=False)
    glucose = db.Column(db.Float(50))
    description = db.Column(db.String(500))
    experiments = db.relationship('Experiment', backref='owner_method', lazy='dynamic')

"""
  backref creates a virtual column in the class specified in the string so that by referencing e.g. experiment1.owner
  you can see who the owner is (the enzyme instance). lazy allows you to find out all the experiments that the Enzyme
  instance has e.g. by running the query: [i.name for i in enzyme1.experiments.all()]
"""

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(800))
    hours = db.Column(db.String(200))
    dp3plus = db.Column(db.String(200))
    dp2 = db.Column(db.String(200))
    glu = db.Column(db.String(200))
    gal = db.Column(db.String(200))
    dp2split = db.Column(db.String(200))
    enzyme_id = db.Column(db.Integer, db.ForeignKey('enzyme.id'))
    method_id = db.Column(db.Integer, db.ForeignKey('method.id'))

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('config.py')
    db.init_app(app)
    with app.app_context():
        return app
