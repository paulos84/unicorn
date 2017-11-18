from flask import Blueprint, render_template, redirect, request, make_response
from wtforms import StringField, FloatField, SelectField, TextAreaField
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired, Regexp
from werkzeug.utils import secure_filename
import pandas as pd
from app import Enzyme, Experiment, Method, db

exp_form = Blueprint('exp_form', __name__)

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
    lactose = FloatField('Lactose monohydrate (g)', default=404, validators=[InputRequired('Lactose amount required')])
    water = FloatField('Water (g)', default=225.6, validators=[InputRequired('Water amount required')])
    glucose = FloatField('Glucose (g)', default=0)
    description = TextAreaField('Notes on experiment procedure')
    file = FileField('Results csv file', validators=[FileRequired(), FileAllowed(['csv'], 'csv files only')])

@exp_form.route('/unicorn/create', methods=['GET', 'POST'])
def create_exp():
    if request.authorization and request.authorization.username == 'admin' and request.authorization.password == 'kong':
        form = ExperimentForm()
        if form.validate_on_submit():
            exp_data = {key: form.data[key] for key in form.data if key in ('name', 'date', 'notes')}
            enz_dict = {'name': form.data['enz_name'], 'dose': form.data['enz_dose']}
            filename = exp_data['name'] + '_results_' + secure_filename(form.file.data.filename)
            form.file.data.save('uploads/' + filename)
            df = pd.read_csv('uploads/{}'.format(filename))
            df.columns = df.columns.str.strip()
            labels = ['hours', 'dp3plus', 'dp2', 'glu', 'gal', 'dp2split']
            results_dict = {a: [','.join([str(b) for b in df[a.strip()]])][0] for a in labels}
            exp_data.update(results_dict)
            method_dict = {key: form.data[key] for key in form.data if key in
                           ('temp', 'lactose', 'water', 'glucose', 'description')}
            method = Method.query.filter_by(**method_dict).first()
            if not method:
                method = Method(**method_dict)
            enzyme = Enzyme.query.filter_by(**enz_dict).first()
            if not enzyme:
                enzyme = Enzyme(**enz_dict)
            exp = Experiment(**exp_data, owner_enzyme=enzyme, owner_method=method)
            db.session.add(exp)
            db.session.commit()
            db.session.refresh(exp)
            return redirect('http://127.0.0.1:8080/api/experiment/{}'.format(str(exp.id)))
        return render_template('exp_form.html', form=form)
    return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})