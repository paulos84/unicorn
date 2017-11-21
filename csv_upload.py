from flask import render_template, Blueprint, request, make_response
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename

process_csv = Blueprint('hourly', __name__)

# move following to a blueprint if not depend upon app or db instance
# Function to reprocess results to account for any non-lactose starting material
# Make so that can save the csv onto local computer
class ConvertResultsForm(FlaskForm):
    file = FileField('Results csv file', validators=[FileRequired(), FileAllowed(['csv'], 'csv files only')])


@process_csv.route('/convert-results', methods=['GET', 'POST'])
def convert_results():
    if request.authorization and request.authorization.username == 'admin' and request.authorization.password == 'kong':
        upload_form = ConvertResultsForm()
        if upload_form.validate_on_submit():
            filename = 'preprocessed_csv_' + secure_filename(upload_form.file.data.filename)
            upload_form.file.data.save('processed_csv/' + filename)
            df = pd.read_csv('processed_csv/{}'.format(filename))
            df.columns = df.columns.str.strip()
            return 'file created'
        return render_template('convert_results.html', form=upload_form)
    return make_response('Unable to verify', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})
