from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restless import APIManager
from flask_migrate import Manager, Migrate, MigrateCommand
from create import exp_create
from models import db, Experiment, Conditions

app = Flask(__name__)
app.config.from_object('config.DevelopmentConfig')



manager = APIManager(app, flask_sqlalchemy_db=db)
# default endpoint: 127.0.0.1:5000/api/experiment
manager.create_api(Experiment, methods=['GET', 'POST', 'PUT', 'DELETE'])
manager.create_api(Conditions, methods=['GET', 'POST', 'PUT', 'DELETE'])

migrate = Migrate(app, db)
db_manager = Manager(app)
db_manager.add_command('db', MigrateCommand)

app.register_blueprint(exp_create)

if __name__ == '__main__':
    app.run(port=8080)
