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
    time = db.Column(db.Float(20))
    dp3 = db.Column(db.Float(20))
    dp2_split = db.Column(db.Float(20))
    dp2 = db.Column(db.Float(20))
    glu = db.Column(db.Float(20))
    gal = db.Column(db.Float(20))
    exp = db.relationship('Results', backref='results', lazy='dynamic')


class ExperimentForm(FlaskForm):
    name = StringField('Experiment name', validators=[InputRequired('Experiment name is required'),
                                                      Length(max=50, message='Max 50 characters')])
    file = FileField()


@app.route('/api/create', methods=['GET', 'POST'])
def create_exp():
    form = ExperimentForm()
    if form.validate_on_submit():
        name = form.data.get('name')
        filename = secure_filename(form.file.data.filename)
        form.file.data.save('uploads/' + filename)
        return filename
    return render_template('exp_form.html', form=form)


if __name__ == '__main__':
    app.run(port=8000, threaded=True)
