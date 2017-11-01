from flask import Flask, request, render_template, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, FloatField
from flask_wtf.file import FileField
from wtforms.validators import InputRequired, Length
from werkzeug.utils import secure_filename
import os
import pandas as pd


app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')
db = SQLAlchemy(app)


class Results(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    times = db.Column(db.String(200))
    dp3 = db.Column(db.String(200))
    dp2_split = db.Column(db.String(200))
    dp2 = db.Column(db.String(200))
    glu = db.Column(db.String(200))
    gal = db.Column(db.String(200))


class ExperimentForm(FlaskForm):
    name = StringField('Experiment name', validators=[InputRequired('Experiment name is required'),
                                                      Length(max=50, message='Max 50 characters')])
    file = FileField()


@app.route('/api/create', methods=['GET', 'POST'])
def create_exp():
    exp_form = ExperimentForm()
    if exp_form.validate_on_submit():
        name = exp_form.data.get('name')
        filename = secure_filename(exp_form.file.data.filename)
        exp_form.file.data.save('uploads/' + filename)
        df = pd.read_csv('uploads/{}'.format(filename))
        labels = ['times', 'dp3', 'dp2_split', 'dp2', 'glu', 'gal']
        results_dict = {a: [','.join([str(b) for b in df[a]])][0] for a in labels}
        # if results_dict['dp2_split'] == '', replace with '0'
        results = Results(**results_dict)
        db.session.add(results)
        db.session.commit()
        return str(results.id)
    return render_template('exp_form.html', form=exp_form)


if __name__ == '__main__':
    app.run(port=8000, threaded=True)
