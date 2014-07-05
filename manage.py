from flask.ext.script import Manager

from app import app

from database import manager as database_manager

manager = Manager(app)
manager.add_command('database', database_manager)


if __name__ == '__main__':
    manager.run()
