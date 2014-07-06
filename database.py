from flask.ext.script import Manager

from instagram.client import InstagramAPI

from app import db, models

manager = Manager(usage='Perform database operations')

@manager.command
def create(populate_tables=True):
    'Create db tables'
    models.db.create_all()
    if populate_tables:
        populate()


@manager.command
def populate(client_id, client_secret):
    'Populate database with default data'
    api = InstagramAPI(client_id=client_id, client_secret=client_secret)

