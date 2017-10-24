from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_migrate import Manager, Migrate, MigrateCommand


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    notes = db.Column(db.String(500))
    dat = db.Column(db.Integer, db.ForeignKey('data.id'))
    cond = db.Column(db.Integer, db.ForeignKey('conditions.id'))


# hold just single peak dp3/gos instead of sequence - allow query - use int or float?
class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dp3 = db.Column(db.Float(200))
    gos = db.Column(db.Float(200))
    exp = db.relationship('Experiment', backref='data', lazy='dynamic')


class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float(10), nullable=False)
    pH = db.Column(db.Float(10))
    enz_dose = db.Column(db.Float(20), nullable=False)
    misc = db.Column(db.String(200), nullable=False)
    exp = db.relationship('Experiment', backref='conditions', lazy='dynamic')


manager = APIManager(app, flask_sqlalchemy_db=db)

# default endpoint: 127.0.0.1:5000/api/experiment
manager.create_api(Experiment, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Data, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Conditions, methods=['GET', 'POST', 'PUT', 'DELETE'])

migrate = Migrate(app, db)
db_manager = Manager(app)
db_manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    app.run(port=8080)
