from flask.ext.testing import TestCase as Base

from app import create_app, db


class TestCase(Base):

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True

    def create_app(self):
        # Pass in test configurations
        return create_app(self)

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
