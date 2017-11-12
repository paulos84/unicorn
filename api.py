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


 # The parent in a one-to-one relationship with Experiment
class Enzyme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dose = db.Column(db.Float(50), nullable=False)
    experiments = db.relationship('Experiment', backref='owner_enzyme', lazy='dynamic')
    """
    backref creates a virtual column in the class specified in the string so that by referencing e.g. experiment1.owner
    you can see who the owner is (the enzyme instance). lazy allows you to find out all the experiments that the Enzyme
    instance has e.g. by running the query: [i.name for i in enzyme1.experiments.all()]
    """


class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float(50), nullable=False)
    lactose = db.Column(db.Float(50), nullable=False)
    water = db.Column(db.Float(50), nullable=False)
    glucose = db.Column(db.Float(50))
    description = db.Column(db.String(800))
    experiments = db.relationship('Experiment', backref='owner_method', lazy='dynamic')


#one-to-one relationship with results
class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    enzyme = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(800))
    enzyme_id = db.Column(db.Integer, db.ForeignKey('enzyme.id'))
    method_id = db.Column(db.Integer, db.ForeignKey('method.id'))
    results_id = db.Column(db.Integer, db.ForeignKey('results.id'))
    results = db.relationship('ResultsSet', backref='owner', lazy='dynamic')


class ResultsSet(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.String(200))
    dp3plus = db.Column(db.String(200))
    dp2 = db.Column(db.String(200))
    glu = db.Column(db.String(200))
    gal = db.Column(db.String(200))
    dp2split = db.Column(db.String(200))
    experiment_id = db.Column(db.Integer, db.ForeignKey('experiment.id'))


manager = APIManager(app, flask_sqlalchemy_db=db)
# default endpoint: 127.0.0.1:8080/api/experiment
manager.create_api(Enzyme, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Experiment, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Method, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(ResultsSet, methods=['GET', 'POST', 'PUT', 'DELETE'])


class ExperimentForm(FlaskForm):
    name = StringField('Experiment name', default='Exp', validators=[InputRequired('Experiment name is required')])
    date = StringField('Date of experiment', validators=[InputRequired('Date format e.g. 2017-10-01')])
    notes = StringField('Notes on aim, summary etc.')
    temp = FloatField("Temp ('C)", validators=[InputRequired('Temperature value required')])
    enz = QuerySelectField(query_factory='', allow_blank=False, label='')
    dose = FloatField('Enzyme dose (mg/g)', validators=[InputRequired('Enzyme dose required')])
    lac = FloatField('Lactose monohydrate (g)', default='404', validators=[InputRequired('Lactose amount required')])
    h2o = FloatField('Water (g)', default='225.6', validators=[InputRequired('Water amount required')])
    glu = FloatField('Glucose (g)')
    desc = StringField('Notes on experiment procedure')
    file = FileField('Results csv file', validators=[FileRequired(), FileAllowed(['csv'], 'csv files only')])


def add_results(filename):
    df = pd.read_csv('uploads/{}'.format(filename))
    df.columns = df.columns.str.strip()
    labels = ['time', 'dp3plus', 'dp2', 'glu', 'gal', 'dp2split']
    results_dict = {a.strip(): [','.join([str(b) for b in df[a.strip()]])][0] for a in labels}
    results = ResultsSet(**results_dict)
    db.session.add(results)
    db.session.commit()
    return results.id


@app.route('/api/create', methods=['GET', 'POST'])
def create_exp():
    form = ExperimentForm()
    if form.validate_on_submit():
        data = {key: form.data[key] for key in form.data if key in ('name', 'date', 'notes')}
        enzyme_id = 1
        data['enzyme'] = {'id': enzyme_id}
        filename = data['name'] + '_results_' + secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        data['results'] = {'id': add_results(filename)}
        url = 'http://127.0.0.1:8080/api/experiment'
        method = {key: form.data[key] for key in form.data if key in ('temp', 'enz', 'lac', 'h2o', 'glu', 'desc')}
        qs = Method.query.filter_by(temp=method['temp'], enzyme=method['enz'], lactose=method['lac'], 
                                    water=method['h2o'], glucose=method['glu'], description=method['desc']).first()
        if qs:
            data['method'] = {'id': qs.id}
            requests.post(url, json=data)
            return jsonify(data)
        data['method'] = method
        requests.post(url, json=data)
        return jsonify(data)
    return render_template('exp_form.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, threaded=True)
