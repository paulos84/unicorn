from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Length
from flask_migrate import Manager, Migrate, MigrateCommand
import requests


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


class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float(10), nullable=False)
    enz_dose = db.Column(db.Float(20), nullable=False)
    misc = db.Column(db.String(500))
    exp = db.relationship('Experiment', backref='conditions', lazy='dynamic')


manager = APIManager(app, flask_sqlalchemy_db=db)
# default endpoint: 127.0.0.1:5000/api/experiment
manager.create_api(Experiment, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Conditions, methods=['GET', 'POST', 'PUT', 'DELETE'])


class ExperimentForm(FlaskForm):
    name = StringField('Experiment name', validators=[InputRequired('Experiment name is required'),
                                                      Length(max=50, message='Max 50 characters')])
    notes = StringField('Notes on aim, summary etc.', validators=[Length(max=500, message='Max 500 characters')])
    dp3 = FloatField('Max DP3 value', validators=[InputRequired('Value required')])
    gos = FloatField('Max GOS value', validators=[InputRequired('Value required')])
    graph_loc = StringField('Graph location', validators=[Length(max=200, message='Max 200 characters')])
    temp = FloatField("Temp ('C)", validators=[InputRequired('Temperature value required')])
    enz_dose = FloatField('Enzyme dose (g)', validators=[InputRequired('Enzyme dose required')])
    misc = StringField('Graph location', validators=[Length(max=500, message='Max 500 characters')])

# remove graph_loc and make dp3 and gos csv string and make a column called intervals(required=False) e.g. hourly
# with viewing to using plotly api
# set up so run and store data locally on s mans comp...pip install requirements

@app.route('/api/create', methods=['GET', 'POST'])
def create_exp():
    form = ExperimentForm()
    if form.validate_on_submit():
        data = {key: form.data[key] for key in form.data if key in ('name', 'notes', 'dp3', 'gos', 'graph_loc')}
        cond = {key: form.data[key] for key in form.data if key in ('temp', 'enz_dose', 'misc')}
        url = 'http://127.0.0.1:8080/api/experiment'
        qs = Conditions.query.filter_by(temp=cond['temp'], enz_dose=cond['enz_dose'], misc=cond['misc']).first()
        if qs:
            data['conditions'] = {'id': qs.id}
            requests.post(url, json=data)
            return jsonify(data)
        data['conditions'] = cond
        requests.post(url, json=data)
        return jsonify(data)
    return render_template('exp_form.html', form=form)


migrate = Migrate(app, db)
db_manager = Manager(app)
db_manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    app.run(port=8080, threaded=True)
