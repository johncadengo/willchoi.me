from datetime import date
from dateutil.relativedelta import relativedelta

from . import db
from .models import Photo


def get_years():
    """Generator that yields a sample photo and date range from each year and
    stops iteration when it reaches the latest photo in the database.

    For example, if the first photo in the database is Feb 29, 2012 and the
    last is Jul 21, 2014, then it will return 3 date ranges:

        Feb 29, 2012 - Feb 28, 2013
        Mar 1, 2013 - Feb 28, 2014
        Mar 1, 2014 - Feb 28, 2015

    Each result will contain a tuple of the sample photo, a start date, and an
    end date. Note the last end date is in the future.
    """
    photo = db.session.query(Photo).order_by(Photo.created_time).first()
    start = photo.created_time.date()
    while True:
        if start.day != 1:
            first_day_of_month = date(start.year, (start.month + 1) % 12, 1)
        else:
            first_day_of_month = start

        end = first_day_of_month + relativedelta(years=1) - relativedelta(days=1)

        yield photo, start, end
        start = end + relativedelta(days=1)
        photo = db.session.query(Photo).filter(
            Photo.created_time>=start
        ).order_by(Photo.created_time).first()
