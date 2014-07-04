from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix


app = Flask(__name__, instance_relative_config=True)
app.config.from_object('config')

try:
    app.config.from_pyfile('config.py')
except IOError:
    pass

app.wsgi_app = ProxyFix(app.wsgi_app)


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
