from flask import request, jsonify, Blueprint, render_template
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
from wtforms.validators import InputRequired, Length
import requests
import json

exp_create = Blueprint('create_experiment', __name__)


class ExperimentForm(FlaskForm):
    name = StringField('Experiment name', validators=[InputRequired('Experiment name is required'),
                                                      Length(max=50, message='Max 50 characters')])
    notes = StringField('Notes on aim, summary etc.', validators=[Length(max=500, message='Max 500 characters')])
    dp3 = FloatField('Max DP3 value', validators=[InputRequired('Value required')])
    gos = FloatField('Max GOS value', validators=[InputRequired('Value required')])
    graph_loc = StringField('Graph location', validators=[Length(max=200, message='Max 200 characters')])
    temp = FloatField("Temp ('C)", validators=[InputRequired('Temperature value required')])
    enz_dose = FloatField('Enzyme dose (g)', validators=[InputRequired('Enzyme dose required')])


@exp_create.route('/create', methods=['GET', 'POST'])
def create_exp():
    exp_form = ExperimentForm()
    name = request.form.get('name')
    notes = request.form.get('notes')
    dp3 = request.form.get('dp3')
    gos = request.form.get('gos')
    graph_loc = request.form.get('graph_loc')
    temp = request.form.get('temp')
    enz_dose = request.form.get('enz_dose')
    if exp_form.validate_on_submit():
        return 'success {}'.format(name)
    return render_template('exp_form.html', form=exp_form)


"""
    if form.validate_on_submit():
        return 'The username is {}. The password is {}'.format (form.username.data, form.password.data)
    return render_template('form.html', form=form)


payload = {
    'title': "The Eye of the World",
    'author': {
        'first_name': "Robert",
        'last_name': "Jordan"
        },
    'is_available': True
}
headers = {'content-type': 'application/json'}
r = requests.post("http://localhost:5000/api/book", data=json.dumps(payload),headers=headers)




class LoginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')


@catalog.route('/form', methods=['GET', 'POST'])
def form():
    form = LoginForm()

    if form.validate_on_submit():
        return 'The username is {}. The password is {}'.format (form.username.data, form.password.data)
    return render_template('form.html', form=form)



@catalog.route('/products')
def products():
    products = Product.query.all()
    res = {}
    for product in products:
        res[product.id] = {
            'name': product.name,
            'price': str(product.price)
                            }
    return jsonify(res)

"""
