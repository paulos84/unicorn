from app import create_app
from app.models import db

from flask_migrate import Manager, Migrate, MigrateCommand


app = create_app()

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

manager.run()
