from flask import render_template, Blueprint, request, make_response
from flask_wtf import FlaskForm
from wtforms import FloatField
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import pandas as pd

process_csv = Blueprint('hourly', __name__)


# Function to reprocess results to account for any non-lactose starting material
# Write a description and example html format on html page
# Make so that can save the csv onto local computer
class ConvertResultsForm(FlaskForm):
    lactose = FloatField('Lactose monohydrate (g)', default=404, validators=[InputRequired('Lactose amount required')])
    glucose = FloatField('Glucose (g)', validators=[InputRequired('Water amount required')])
    file = FileField('Results csv file', validators=[FileRequired(), FileAllowed(['csv'], 'csv files only')])


@process_csv.route('/convert-results', methods=['GET', 'POST'])
def convert_results():
    if request.authorization and request.authorization.username == 'admin' and request.authorization.password == 'kong':
        upload_form = ConvertResultsForm()
        if upload_form.validate_on_submit():
            glu_conc = upload_form.data['glucose'] / (upload_form.data['lactose'] * 0.95 + upload_form.data['glucose'])
            filename = 'preprocessed_csv_' + secure_filename(upload_form.file.data.filename)
            upload_form.file.data.save('processed_csv/' + filename)
            df = pd.read_csv('processed_csv/{}'.format(filename))
            df.columns = df.columns.str.strip()
            return 'Results csv file created to account for glucose as {}% of total solids'.format(str(glu_conc*100))
        return render_template('convert_results.html', form=upload_form)
    return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
