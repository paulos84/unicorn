from flask import request, jsonify, Blueprint, render_template
from api import db, Experiment, Conditions
from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, FloatField
import requests
import json

exp_create = Blueprint('create_experiment', __name__)



class ExperimentForm(FlaskForm):
    name = StringField('name')
    notes = StringField('notes')
    dp3 = FloatField('dp3')
    gos = FloatField('gos')
    graph_loc = StringField('graph_loc')




#@catalog.route('/product-create', methods=['POST',])
#def create_product():
@exp_create.route('/exp-create', methods=['POST', ])
def create_exp():
    name = request.form.get('name')
    price = request.form.get('price')
    product = Product(name, price)
    db.session.add(product)
    db.session.commit()
    return 'Product created.'



@catalog.route('/form', methods=['GET', 'POST'])
def product_form():
    form = ProductForm()

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



"""
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
