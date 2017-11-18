from flask import make_response
from app.charts import charts
from app.exp_form import exp_form
from flask import request
from flask_restless import APIManager, ProcessingException
from app import create_app, db, Enzyme, Method, Experiment

app = create_app()
app.register_blueprint(exp_form)
app.register_blueprint(charts)


def check_credentials(**kwargs):
    if request.authorization and request.authorization.username == 'admin' and request.authorization.password == 'kong':
        return make_response('Could not verify!', 401, {'WWW-Authenticate': 'Basic realm="Login Required"'})


with app.app_context():
    db.init_app(app)

    access_password = 'mysecretkey'



    manager = APIManager(app, flask_sqlalchemy_db=db)
    http_methods = ['GET', 'POST', 'PUT', 'DELETE']
    protected = ['POST', 'PUT_SINGLE', 'PUT-MANY', 'DELETE_SINGLE', 'DELETE_MANY']
    enz_api = manager.create_api(Enzyme, methods=http_methods,
                                           preprocessors={a: [check_credentials] for a in protected})
    method_api = manager.create_api(Method, methods=http_methods,
                                              preprocessors={a: [check_credentials] for a in protected})
    exp_api = manager.create_api(Experiment, methods=http_methods,
                                           preprocessors={a: [check_credentials] for a in protected})

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1', port=8080, passthrough_errors=True)