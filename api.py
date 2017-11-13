from flask import Flask, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DecimalField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
from flask_restless import APIManager
import pandas as pd



# To Do - login password protection  - how to do with Flask-Restful/restless?
# Use regex validators for form to ensure date format 2017-10-16
# remove unused relationships?
# produce schema on paper showing relationships


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


class Enzyme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dose = db.Column(db.Float(50), nullable=False)
    experiments = db.relationship('Experiment', backref='owner_enzyme', lazy='dynamic')

class Method(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float(50), nullable=False)
    lactose = db.Column(db.Float(50), nullable=False)
    water = db.Column(db.Float(50), nullable=False)
    glucose = db.Column(db.Float(50))
    description = db.Column(db.String(500))
    experiments = db.relationship('Experiment', backref='owner_method', lazy='dynamic')
"""
  backref creates a virtual column in the class specified in the string so that by referencing e.g. experiment1.owner
  you can see who the owner is (the enzyme instance). lazy allows you to find out all the experiments that the Enzyme
  instance has e.g. by running the query: [i.name for i in enzyme1.experiments.all()]
"""

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    enz_name = db.Column(db.String(50), nullable=False)
    enz_dose = db.Column(db.Float(50), nullable=False)
    notes = db.Column(db.String(800))
    hours = db.Column(db.String(200))
    dp3plus = db.Column(db.String(200))
    dp2 = db.Column(db.String(200))
    glu = db.Column(db.String(200))
    gal = db.Column(db.String(200))
    dp2split = db.Column(db.String(200))
    enzyme_id = db.Column(db.Integer, db.ForeignKey('enzyme.id'))
    method_id = db.Column(db.Integer, db.ForeignKey('method.id'))


manager = APIManager(app, flask_sqlalchemy_db=db)
# default endpoint: 127.0.0.1:8080/api/experiment
manager.create_api(Enzyme, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Method, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Experiment, methods=['GET', 'POST', 'PUT', 'DELETE'])


class ExperimentForm(FlaskForm):
    name = StringField('Experiment name', default='Exp', validators=[InputRequired('Experiment name is required')])
    date = StringField('Date of experiment', validators=[InputRequired('Date format e.g. 2017-10-01')])
    notes = TextAreaField('Notes on aim, summary etc.')
    enz_name = SelectField(choices=[('wu', 'White unicorn'), ('gc288', 'GC288'), ('godo', 'GODO YNL-2')],
                           validators=[InputRequired('Enzyme name required')])
    enz_dose = FloatField('Enzyme dose (mg/g)', validators=[InputRequired('Enzyme dose required')])
    temp = FloatField("Temp ('C)", validators=[InputRequired('Temperature value required')])
    lac = FloatField('Lactose monohydrate (g)', default='404', validators=[InputRequired('Lactose amount required')])
    h2o = FloatField('Water (g)', default='225.6', validators=[InputRequired('Water amount required')])
    glu = FloatField('Glucose (g)')
    desc = TextAreaField('Notes on experiment procedure')
    file = FileField('Results csv file', validators=[FileRequired(), FileAllowed(['csv'], 'csv files only')])


@app.route('/api/create', methods=['GET', 'POST'])
def create_exp():
    form = ExperimentForm()
    if form.validate_on_submit():
        exp_data = {key: form.data[key] for key in form.data if key in ('name', 'date', 'notes')}
        enz_dict = {key: form.data[key] for key in form.data if key in ('enz_name', 'enz_dose')}
        filename = exp_data['name'] + '_results_' + secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        df = pd.read_csv('uploads/{}'.format(filename))
        df.columns = df.columns.str.strip()
        labels = ['hours', 'dp3plus', 'dp2', 'glu', 'gal', 'dp2split']
        results_dict = {a.strip(): [','.join([str(b) for b in df[a.strip()]])][0] for a in labels}
        exp_data.update(results_dict)
        method_dict = {key: form.data[key] for key in form.data if key in ('temp', 'lac', 'h2o', 'glu', 'desc')}
        method = Method.query.filter_by(
            temp=method_dict['temp'], lactose=method_dict['lac'], water=method_dict['h2o'], glucose=method_dict['glu'],
            description=method_dict['desc']).first()
        enzyme = Enzyme.query.filter_by(name=enz_dict['enz_name'], dose=enz_dict['enz_dose'])
        if method_query and enzyme_query:
            #do not need to create new db entry from method and enzyme, just reference the method_query and enz_
            exp = Experiment(**exp_data, owner_enzyme=enzyme, owner_method=method)
            #db.add with backref to parent method
            #       exp = Experiment(**exp_data.update())
            return jsonify(exp_data)
            # return a view of the exp data just entered, RESTLess route?
        #else db.session.add each separately and then backref one in the other   --  see example from aurn-api
        return jsonify(exp_data)
    return render_template('exp_form.html', form=form)


if __name__ == '__main__':
    app.run(port=8080, threaded=True)
