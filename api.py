from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_migrate import Manager, Migrate, MigrateCommand
from create import exp_create

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


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


manager = APIManager(app, flask_sqlalchemy_db=db)
# default endpoint: 127.0.0.1:5000/api/experiment
manager.create_api(Experiment, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Conditions, methods=['GET', 'POST', 'PUT', 'DELETE'])

migrate = Migrate(app, db)
db_manager = Manager(app)
db_manager.add_command('db', MigrateCommand)

app.register_blueprint(exp_create)

if __name__ == '__main__':
    app.run(port=8080)
