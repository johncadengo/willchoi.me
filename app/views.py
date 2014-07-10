from flask import render_template

from . import app, db
from .models import Photo, Image


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
    # Get the first photo from each year
    photos = db.session.query(Photo).filter(
                Photo.created_time>'2013-06-01'
            ).order_by(Photo.created_time).limit(3).all()
    images = [photo.standard_res_image.url for photo in photos]

    return render_template('photo-a-day-series.html', images=images)
