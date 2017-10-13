from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    aim = db.Column(db.String(300))
    results_loc =  db.Column(db.String(300))
    summary = db.Column(db.String(500))
    enzyme_id = db.Column(db.Integer, db.ForeignKey('enzyme.id'))
    conditions_id = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    reactants_id = db.Column(db.Integer, db.ForeignKey('reactants.id'))

class Enzyme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    batch = db.Column(db.String(50))
    amount = db.Column(db.Float(20), nullable=False)
    experiment = db.relationship('Experiment', backref='enzyme', lazy='dynamic')


class Reactants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    r1_name = db.Column(db.String(50), nullable=False)
    r1_batch = db.Column(db.String(50))
    r1_amount = db.Column(db.Float(20), nullable=False)
    r2_name = db.Column(db.String(50))
    r2_batch = db.Column(db.String(50))
    r2_amount = db.Column(db.Float(20))
    experiment = db.relationship('Experiment', backref='reactants', lazy='dynamic')
    #e.g. first instance = lactose, bn ...., amount=280g
    ##    2nd instance   = water, (null), amount - 170g
    ## views - concentration - calculate from amounts


class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float(10))
    pH = db.Column(db.Float(10))
    experiment = db.relationship('Experiment', backref='conditions', lazy='dynamic')
