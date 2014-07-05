from flask.ext.script import Manager

from app import db, models

manager = Manager(usage='Perform database operations')


@manager.command
def populate():
    "Populate database with default data"
    print "hello"
