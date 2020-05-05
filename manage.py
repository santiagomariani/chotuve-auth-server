from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_failsafe import failsafe

from run import app
from app import db

@failsafe
def create_app():
  return app

migrate = Migrate(app, db)
manager = Manager(create_app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()