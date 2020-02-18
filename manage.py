import os
import unittest

from main import create_app, db

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager

from models import User


env = os.getenv("ENVIRON_TYPE" or "dev")
app = create_app(env)
app.app_context().push()

manager = Manager(app)

migrate = Migrate(app, db)
manager.add_command("db", MigrateCommand)


@manager.command
def run():
    from main import views


@manager.command
def test():
    tests = unittest.TestLoader().discover("tests", pattern="test*.py")
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


if __name__ == "__main__":
    manager.run()
