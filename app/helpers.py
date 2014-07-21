from . import db
from .models import Photo


def get_years():
    """Generator that yields a sample photo and date range from each year and
    stops iteration when it reaches the latest photo in the database.

    For example, if the first photo in the database is Feb 29, 2012 and the
    last is Jul 21, 2014, then it will return 3 date ranges:

        Feb 29, 2012 - Feb 28, 2013
        Mar 1, 2013 - Feb 28, 2014
        Mar 1, 2014 - Present

    Each result will contain a tuple of the sample photo, a start date, and an
    end date.
    """
    first_photo = db.session.query(Photo).order_by(Photo.created_time).first()
    while True:
        yield first_photo
