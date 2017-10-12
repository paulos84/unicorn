from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Experiment(db.Model):
    __tablename__ = 'experiments'
    id = db.Column(db.Integer, primary_key=True)
    aim = db.Column(db.String(300), unique=True)
    enzyme_id = db.Column(db.Integer, db.ForeignKey('enzymes.id'), nullable=False)
    conditions_id = db.Column(db.Integer, db.ForeignKey('conditions.id'), nullable=False)
    reactants_id = db.Column(db.Integer, db.ForeignKey('reactants.id'), nullable=False)


class Enzyme(db.Model):
    __tablename__ = 'enzymes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    batch = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.String(50), nullable=False)
    experiment = db.relationship('Experiment', backref='owner', lazy='dynamic')


class Reactant(db.Model):
    __tablename__ = 'reactants'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    batch = db.Column(db.String(50))
    amount = db.Column(db.Float(20), nullable=False)
    #e.g. first instance = lactose, bn ...., amount=280g
    ##    2nd instance   = water, (null), amount - 170g
    ## views - concentration - calculate from amounts


class Conditions(db.Model):
    __tablename__ = 'conditions'
    id = db.Column(db.Integer, primary_key=True)
    temperature = db.Column(db.Float(10))
    pH = db.Column(db.Float(10))
    experiment = db.relationship('Experiment', backref='owner', lazy='dynamic')

