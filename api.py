from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_migrate import Manager, Migrate, MigrateCommand


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    notes = db.Column(db.String(500))
    dat = db.Column(db.Integer, db.ForeignKey('data.id'))
    enz = db.Column(db.Integer, db.ForeignKey('enzyme.id'))
    cond = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    react = db.Column(db.Integer, db.ForeignKey('reactants.id'))


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dp3 = db.Column(db.String(200))
    gos = db.Column(db.String(200))
    times = db.Column(db.String(100))
    exp = db.relationship('Experiment', backref='data', lazy='dynamic')


class Enzyme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    batch = db.Column(db.String(50))
    amount = db.Column(db.Float(20), nullable=False)
    exp = db.relationship('Experiment', backref='enzyme', lazy='dynamic')


class Reactants(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    lac = db.Column(db.Float(20), nullable=False)
    batch = db.Column(db.String(50))
    water = db.Column(db.Float(20), nullable=False)
    exp = db.relationship('Experiment', backref='reactants', lazy='dynamic')


class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float(10))
    pH = db.Column(db.Float(10))
    exp = db.relationship('Experiment', backref='conditions', lazy='dynamic')


manager = APIManager(app, flask_sqlalchemy_db=db)

# default endpoint: 127.0.0.1:5000/api/experiment
manager.create_api(Experiment, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Enzyme, methods=['GET', 'POST', 'PUT', 'DELETE'])

migrate = Migrate(app, db)
db_manager = Manager(app)
db_manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    app.run()




