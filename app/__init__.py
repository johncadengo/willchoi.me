from flask import Flask, render_template
from flask.ext.sqlalchemy import SQLAlchemy

from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

try:
    app.config.from_pyfile('config.py')
except IOError:
    pass

app.wsgi_app = ProxyFix(app.wsgi_app)

db = SQLAlchemy(app)

# Late import so dependencies work right
from . import models

# Populate database on the first request. May take awhile.
@app.before_first_request
def before_first_request():
    try:
        models.db.create_all()
    except Exception, e:
        app.logger.error(str(e))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/art/")
def art():
    return render_template('art.html')


@app.route("/blog/")
def blog():
    return render_template('blog.html')


@app.route("/contact/")
def contact():
    return render_template('contact.html')


@app.route("/design/")
def design():
    return render_template('design.html')


@app.route("/photo/")
def photo():
    return render_template('photo.html')


@app.route("/photo-a-day-series/")
def photo_a_day_series():
    return render_template('photo-a-day-series.html')
