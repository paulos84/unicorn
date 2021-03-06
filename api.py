from flask import Flask, render_template, redirect, request, make_response
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, TextAreaField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Regexp
from werkzeug.utils import secure_filename
from flask_restless import APIManager, ProcessingException
import pandas as pd
from csv_upload import process_csv

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
app.register_blueprint(process_csv)
db = SQLAlchemy(app)

class Enzyme(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    dose = db.Column(db.Float(50), nullable=False)
    experiments = db.relationship('Experiment', backref='owner_enzyme', lazy='dynamic')

class ConditionsSet(db.Model):
    __tablename__ = 'conditions'
    id = db.Column(db.Integer, primary_key=True)
    temp = db.Column(db.Float(50), nullable=False)
    pH = db.Column(db.Float(10))
    lactose = db.Column(db.Float(50), nullable=False)
    water = db.Column(db.Float(50), nullable=False)
    glucose = db.Column(db.Float(50))
    experiments = db.relationship('Experiment', backref='owner_conditions', lazy='dynamic')

    def lactose_concentration(self):
        return self.lactose/(self.water+self.lactose) * 100
"""
  backref creates a virtual column in the class specified in the string so that by referencing e.g. experiment1.owner
  you can see who the owner is (the enzyme instance). lazy allows you to find out all the experiments that the Enzyme
  instance has e.g. by running the query: [i.name for i in enzyme1.experiments.all()]
"""

class Experiment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    date = db.Column(db.String(50), nullable=False)
    notes = db.Column(db.String(800))
    procedure_notes = db.Column(db.String(800))
    hours = db.Column(db.String(200))
    dp3plus = db.Column(db.String(200))
    dp2 = db.Column(db.String(200))
    glu = db.Column(db.String(200))
    gal = db.Column(db.String(200))
    dp2split = db.Column(db.String(200))
    enzyme_id = db.Column(db.Integer, db.ForeignKey('enzyme.id'))
    conditions_id = db.Column(db.Integer, db.ForeignKey('conditions.id'))

access_password = 'mysecretkey'

def check_credentials(**kwargs):
    if request.headers.get('X-Secret-Key', '') != access_password:
        raise ProcessingException(code=401)

manager = APIManager(app, flask_sqlalchemy_db=db)

include_methods = ['lactose_concentration']
http_methods = ['GET', 'POST', 'PUT', 'DELETE']
protected = ['POST', 'PUT_SINGLE', 'PUT MANY', 'DELETE_SINGLE', 'DELETE_MANY']
manager.create_api(Enzyme, methods=http_methods, preprocessors={a: [check_credentials] for a in protected})
manager.create_api(ConditionsSet, include_methods = ['lactose_concentration'], methods=http_methods,
                   preprocessors={a: [check_credentials] for a in protected})
manager.create_api(Experiment, methods=http_methods, preprocessors={a: [check_credentials] for a in protected})

class ExperimentForm(FlaskForm):
    name = StringField('Experiment name', default='Exp', validators=[InputRequired('Experiment name is required')])
    date = StringField('Date of experiment', validators=[InputRequired(),
                                                         Regexp(r"[0-9]{4}[-]{1}[0-9]{2}[-]{1}[0-9]{2}",
                                                                message='Date format YYYY-MM-DD')])
    notes = TextAreaField('Notes on aim, results etc.')
    enz_name = SelectField(choices=[('wu', 'White unicorn'), ('gc288', 'GC288'), ('godo', 'GODO YNL-2')],
                           validators=[InputRequired('Enzyme name required')])
    enz_dose = FloatField('Enzyme dose (mg/g)', validators=[InputRequired('Enzyme dose required')])
    temp = FloatField("Temp ('C)", validators=[InputRequired('Temperature value required')])
    pH = FloatField('pH value, if adjusted', default=None)
    lactose = FloatField('Lactose monohydrate (g)', default=404, validators=[InputRequired('Lactose amount required')])
    water = FloatField('Water (g)', default=225.6, validators=[InputRequired('Water amount required')])
    glucose = FloatField('Glucose (g)', default=0)
    procedure_notes = TextAreaField('Notes on experiment procedure')
    file = FileField('Results csv file', validators=[FileRequired(), FileAllowed(['csv'], 'csv files only')])

@app.route('/create', methods=['GET', 'POST'])
def create_exp():
    if request.authorization and request.authorization.username == 'admin' and request.authorization.password == 'kong':
        form = ExperimentForm()
        if form.validate_on_submit():
            exp_data = {key: form.data[key] for key in form.data if key in ('name', 'date', 'notes', 'procedure_notes')}
            enz_dict = {'name': form.data['enz_name'], 'dose': form.data['enz_dose']}
            filename = exp_data['name'] + '_results_' + secure_filename(form.file.data.filename)
            form.file.data.save('uploads/' + filename)
            df = pd.read_csv('uploads/{}'.format(filename))
            df.columns = df.columns.str.strip()
            labels = ['hours', 'dp3plus', 'dp2', 'glu', 'gal', 'dp2split']
            results_dict = {a: [','.join([str(b) for b in df[a.strip()]])][0] for a in labels}
            exp_data.update(results_dict)
            conditions_dict = {a: form.data[a] for a in form.data if a in
                           ('temp', 'pH', 'water', 'glucose')}
            conditions_dict['lactose'] = form.data['lactose'] * 0.95
            conditions = ConditionsSet.query.filter_by(**conditions_dict).first()
            if not conditions:
                conditions = ConditionsSet(**conditions_dict)
            enzyme = Enzyme.query.filter_by(**enz_dict).first()
            if not enzyme:
                enzyme = Enzyme(**enz_dict)
            exp = Experiment(**exp_data, owner_enzyme=enzyme, owner_conditions=conditions)
            db.session.add(exp)
            db.session.commit()
            db.session.refresh(exp)
            return redirect('http://127.0.0.1:8080/api/experiment/{}'.format(str(exp.id)))
        return render_template('exp_form.html', form=form)
    return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})

@app.route('/results/<int:exp_id>')
def plot(exp_id, chart_id='chart_ID', chart_type='line', chart_height=550, chart_width=800):
    exp = Experiment.query.filter_by(id=exp_id).first()
    chart = {"renderTo": chart_id, "type": chart_type, "height": chart_height, "width": chart_width}
    series = [{"name": 'DP2', "data": [float(a) for a in exp.dp2.split(',')]},
             {"name": 'DP3+', "data": [float(a) for a in exp.dp3plus.split(',')]}]
    title = {"text": "{}. Conditions: Enzyme: {}, Dose: {} mg/g, Temp: {}'C".format(
        exp.name, exp.owner_enzyme.name, exp.owner_enzyme.dose, exp.owner_conditions.temp)}
    xaxis = {"categories": exp.hours.split(',')}
    yaxis = {"title": {"text": '%'}}
    return render_template('chart.html', chartID=chart_id, chart=chart, series=series, title=title, xAxis=xaxis,
                           yAxis=yaxis)

if __name__ == '__main__':
    app.run(port=8080, threaded=True)
