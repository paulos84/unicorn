from flask import render_template, Blueprint, request, make_response
from flask_wtf import FlaskForm
from wtforms import FloatField, StringField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import pandas as pd

process_csv = Blueprint('process_csv', __name__)


# Write a description and example html format on html page
class ConvertResultsForm(FlaskForm):
    lactose = FloatField('Lactose monohydrate (g)', default=404, validators=[InputRequired('Lactose amount required')])
    glucose = FloatField('Glucose (g)', validators=[InputRequired('Water amount required')])
    name = StringField('Filename for new csv file', validators=[InputRequired('Filename required')])
    file = FileField('Results csv file', validators=[FileRequired(), FileAllowed(['csv'], 'csv files only')])


# Function to reprocess results to account for any non-lactose starting material
@process_csv.route('/convert-results', methods=['GET', 'POST'])
def convert_results():
    if request.authorization and request.authorization.username == 'admin' and request.authorization.password == 'kong':
        upload_form = ConvertResultsForm()
        if upload_form.validate_on_submit():
            try:
                added_glu = upload_form.data['glucose'] / (upload_form.data['lactose'] * 0.95 + upload_form.data['glucose'])
                filename = 'preprocessed_csv_' + secure_filename(upload_form.file.data.filename)
                upload_form.file.data.save('processed_csv/' + filename)
                df = pd.read_csv('processed_csv/{}'.format(filename))
                df.iloc[6, 1:] = df.iloc[6, 1:] - added_glu
                df.iloc[:-1, 1:] = df.iloc[:-1, 1:] / df.iloc[:-1, 1:].sum()
                s1 = df.iloc[:5].sum()
                s1[0] = 'DP3+'
                df = df.append(s1, ignore_index=True)
                s2 = df.iloc[-1, 1:] + df.iloc[5, 1:] * df.iloc[-2, 1:]
                df = df.append(s2, ignore_index=True)
                df.iloc[-1, 0] = 'Total GOS'
                resp = make_response(df.to_csv())
                resp.headers["Content-Disposition"] = "attachment; filename={}.csv".format(upload_form.data['name'])
                resp.headers["Content-Type"] = "text/csv"
                return resp
            except TypeError:
                return 'Incorrect csv file formatting. Please go back and try again.'
        return render_template('convert_results.html', form=upload_form)
    return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})