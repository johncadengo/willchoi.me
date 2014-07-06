from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from werkzeug.contrib.fixers import ProxyFix

db = SQLAlchemy()


def create_app(config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config)

    if not app.config.get('TESTING'):
        try:
            app.config.from_pyfile('config.py')
        except IOError:
            pass

    app.wsgi_app = ProxyFix(app.wsgi_app)

    db.init_app(app) # Don't initalize db until we get configs
    return app

app = create_app('config')


from . import models, views
