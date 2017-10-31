from flask import Flask, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from wtforms.validators import InputRequired, Length
from flask_migrate import Manager, Migrate, MigrateCommand
from flask_wtf.file import FileField
from wtforms.validators import InputRequired, Length
from werkzeug.utils import secure_filename
import requests

import pandas as pd


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
    times = db.Column(db.Float(20))
    dp3 = db.Column(db.Float(20))
    dp2_split = db.Column(db.Float(20))
    dp2 = db.Column(db.Float(20))
    glu = db.Column(db.Float(20))
    gal = db.Column(db.Float(20))
    exp = db.relationship('Experiment', backref='results', lazy='dynamic')


manager = APIManager(app, flask_sqlalchemy_db=db)
# default endpoint: 127.0.0.1:5000/api/experiment
manager.create_api(Experiment, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Conditions, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Results, methods=['GET', 'POST', 'PUT', 'DELETE'])


class ExperimentForm(FlaskForm):
    name = StringField('Experiment name', validators=[InputRequired('Experiment name is required'),
                                                      Length(max=50, message='Max 50 characters')])
    notes = StringField('Notes on aim, summary etc.', validators=[Length(max=500, message='Max 500 characters')])
    temp = FloatField("Temp ('C)", validators=[InputRequired('Temperature value required'), Length(max=20)])
    enz_dose = FloatField('Enzyme dose (g)', validators=[InputRequired('Enzyme dose required', Length(max=20))])
    misc = StringField('Graph location', validators=[Length(max=500, message='Max 500 characters')])
    file = FileField()


def add_results(results_file):
    filename = secure_filename(results_file.data.filename)
    results_file.data.save('uploads/' + filename)
    df = pd.read_csv('uploads/{}'.format(filename))
    labels = ['times', 'dp3', 'dp2_split', 'dp2', 'glu', 'gal']
    results_dict = {a: [','.join([str(b) for b in df[a]])][0] for a in labels}
    # if results_dict['dp2_split'] == '', replace with '0'
    results = Results(**results_dict)
    db.session.add(results)
    db.session.commit()
    return results.id


@app.route('/api/create', methods=['GET', 'POST'])
def create_exp():
    form = ExperimentForm()
    if form.validate_on_submit():
        data = {key: form.data[key] for key in form.data if key in ('name', 'notes', 'dp3', 'gos', 'graph_loc')}
        cond = {key: form.data[key] for key in form.data if key in ('temp', 'enz_dose', 'misc')}
        results_id = add_results(form.file)
        data['results'] = {'id': results_id}
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
