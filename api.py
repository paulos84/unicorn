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
    cond = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    results = db.Column(db.Integer, db.ForeignKey('results.id'))


class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float(10), nullable=False)
    enz_dose = db.Column(db.Float(20), nullable=False)
    misc = db.Column(db.String(500))
    exp = db.relationship('Experiment', backref='conditions', lazy='dynamic')


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Float(20))
    dp3 = db.Column(db.Float(20))
    dp2_split = db.Column(db.Float(20))
    dp2 = db.Column(db.Float(20))
    glu = db.Column(db.Float(20))
    gal = db.Column(db.Float(20))
    exp = db.relationship('Results', backref='results', lazy='dynamic')


manager = APIManager(app, flask_sqlalchemy_db=db)
# default endpoint: 127.0.0.1:5000/api/experiment
manager.create_api(Experiment, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Conditions, methods=['GET', 'POST', 'PUT', 'DELETE'])


class ExperimentForm(FlaskForm):
    name = StringField('Experiment name', validators=[InputRequired('Experiment name is required'),
                                                      Length(max=50, message='Max 50 characters')])
    notes = StringField('Notes on aim, summary etc.', validators=[Length(max=500, message='Max 500 characters')])
    temp = FloatField("Temp ('C)", validators=[InputRequired('Temperature value required'), Length(max=20)])
    enz_dose = FloatField('Enzyme dose (g)', validators=[InputRequired('Enzyme dose required', Length(max=20))])
    misc = StringField('Graph location', validators=[Length(max=500, message='Max 500 characters')])
    results_id = FloatField('Results id')




# remove graph_loc and make dp3 and gos csv string and make a column called intervals(required=False) e.g. hourly
# with viewing to using plotly api
# set up so run and store data locally on s mans comp...pip install requirements

@app.route('/api/create', methods=['GET', 'POST'])
def create_exp():
    exp_form = ExperimentForm()
    if exp_form.validate_on_submit():
        temp = request.form.get('temp')
        enz_dose = request.form.get('enz_dose')
        misc = request.form.get('misc')
        form_data = {a: b for a, b in request.form.items() if a != 'csrf_token' and b != ''}
        exp_data = {key: form_data[key] for key in form_data if key in ('name', 'notes', 'dp3', 'gos', 'graph_loc')}
        conditions = {key: form_data[key] for key in form_data if key in ('temp', 'enz_dose', 'misc')}
        url = 'http://127.0.0.1:8080/api/experiment'
        qs = Conditions.query.filter_by(temp=temp, enz_dose=enz_dose).first()
        if [temp, enz_dose, misc] == [qs.temp, qs.enz_dose, None] or [qs.temp, qs.enz_dose, qs.misc]:
            exp_data['conditions'] = {'id': qs.id}
            requests.post(url, json=exp_data)
            return jsonify(exp_data)
        exp_data['conditions'] = conditions
        requests.post(url, json=exp_data)
        return jsonify(exp_data)
    return render_template('exp_form.html', form=exp_form)


migrate = Migrate(app, db)
db_manager = Manager(app)
db_manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    app.run(port=8080, threaded=True)
