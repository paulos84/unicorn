from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_restless import APIManager
import requests
import pandas as pd
from wtforms_alchemy.fields import QuerySelectField


# To Do - login password protection  - how to do with Flask-Restful/restless?
# Datefield in wtforms to ensure date format 2017-10-16
# remove unused relationships?
# produce schema on paper showing relationships

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


class Enzyme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    enzyme = db.Column(db.String(50), nullable=False)
    dose = db.Column(db.Float(50), nullable=False)
    exp = db.relationship('Experiment', backref='owner', lazy='dynamic')
    # backref means creating virtual column in the class specified in the string e.g. the Experiment class/table
    #  so that by referencing experiment.owner can see who the owner is
    # lazy allows find out all the experiments that the Enzyme instance has by saying e.g. enzyme1.experiments by
    # e.g. for i in enzyme1: print(i.name) - gives list of experiment names


class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    enzyme = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(800))
    enzyme_id = db.Column(db.Integer, db.ForeignKey('enzyme.id'))
    conditions_id = db.Column(db.Integer, db.ForeignKey('conditions.id'))
    results_id = db.Column(db.Integer, db.ForeignKey('results.id'))


class Conditions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float(50), nullable=False)
    lactose = db.Column(db.Float(50), nullable=False)
    water = db.Column(db.Float(50), nullable=False)
    glucose = db.Column(db.Float(50))
    description = db.Column(db.String(800))
    exp = db.relationship('Experiment', backref='conditions', lazy='dynamic')


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(200))
    dp3plus = db.Column(db.String(200))
    dp2 = db.Column(db.String(200))
    glu = db.Column(db.String(200))
    gal = db.Column(db.String(200))
    dp2split = db.Column(db.String(200))


exp = db.relationship('Experiment', backref='conditions', lazy='dynamic')

manager = APIManager(app, flask_sqlalchemy_db=db)
# default endpoint: 127.0.0.1:8080/api/experiment
manager.create_api(Experiment, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Conditions, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Results, methods=['GET', 'POST', 'PUT', 'DELETE'])


class ExperimentForm(FlaskForm):
    name = StringField('Experiment name', default='Exp', validators=[InputRequired('Experiment name is required')])
    date = StringField('Date of experiment', validators=[InputRequired('Date format e.g. 2017-10-01')])
    notes = StringField('Notes on aim, summary etc.')
    temp = FloatField("Temp ('C)", validators=[InputRequired('Temperature value required')])
                        # To do: make way to add new dose or select from choices
    enz = QuerySelectField(query_factory='', allow_blank=False, label='')
    dose = FloatField('Enzyme dose (mg/g)', validators=[InputRequired('Enzyme dose required')])
    lac = FloatField('Lactose monohydrate (g)', default='404', validators=[InputRequired('Lactose amount required')])
    h2o = FloatField('Water (g)', default='225.6', validators=[InputRequired('Water amount required')])
    glu = FloatField('Glucose (g)')
    desc = StringField('Notes relating to conditions')
    file = FileField('Results csv file', validators=[FileRequired(), FileAllowed(['csv'], 'csv files only')])


def add_results(filename):
    df = pd.read_csv('uploads/{}'.format(filename))
    df.columns = df.columns.str.strip()
    labels = ['time', 'dp3plus', 'dp2', 'glu', 'gal', 'dp2split']
    results_dict = {a.strip(): [','.join([str(b) for b in df[a.strip()]])][0] for a in labels}
    results = Results(**results_dict)
    db.session.add(results)
    db.session.commit()
    return results.id


@app.route('/api/create', methods=['GET', 'POST'])
def create_exp():
    form = ExperimentForm()
    if form.validate_on_submit():
        data = {key: form.data[key] for key in form.data if key in ('name', 'date', 'notes')}
        cond = {key: form.data[key] for key in form.data if key in ('temp', 'enz', 'lac', 'h2o', 'glu', 'desc')}
        filename = data['name'] + '_results_' + secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        results_id = add_results(filename)
        data['results'] = {'id': results_id}
        url = 'http://127.0.0.1:8080/api/experiment'
        qs = Conditions.query.filter_by(temp=cond['temp'], enzyme=cond['enz'], lactose=cond['lac'], water=cond['h2o'],
                                        glucose=cond['glu'], description=cond['desc']).first()
        if qs:
            data['conditions'] = {'id': qs.id}
            requests.post(url, json=data)
            return jsonify(data)
        data['conditions'] = cond
        requests.post(url, json=data)
        return jsonify(data)
    return render_template('exp_form.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, threaded=True)
