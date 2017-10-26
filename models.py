from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(500))
    dp3 = db.Column(db.Float(200), nullable=False)
    gos = db.Column(db.Float(200), nullable=False)
    graph_loc = db.Column(db.String(200))
    cond = db.Column(db.Integer, db.ForeignKey('conditions.id'))
# hold just single peak dp3/gos instead of sequence - allow query - use int or float?

class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float(10), nullable=False)
    enz_dose = db.Column(db.Float(20), nullable=False)
    exp = db.relationship('Experiment', backref='conditions', lazy='dynamic')
