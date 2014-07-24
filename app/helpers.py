from calendar import monthrange
from datetime import date
from dateutil.relativedelta import relativedelta

from . import db
from .models import Photo


class Paginator(object):
    def __init__(self, year, month=None, day=None):
        self.year = year
        self.month = month
        self.day = day

        self.first_photo = db.session.query(Photo).order_by(Photo.created_time).first()
        self.last_photo = db.session.query(Photo).order_by(Photo.created_time.desc()).first()

    @property
    def end(self):
        raise NotImplementedError

    def iter_pages(self):
        raise NotImplementedError

    @property
    def page(self):
        raise NotImplementedError

    @property
    def start(self):
        raise NotImplementedError


class YearPaginator(Paginator):
    @property
    def end(self):
        return self.last_photo.created_time.date().year

    def iter_pages(self):
        """Yields a sample photo and date range from each year and stops
        iteration when it reaches the latest photo in the database.

        For example, if the first photo in the database is Feb 29, 2012 and the
        last is Jul 21, 2014, then it will return 3 date ranges:

            Feb 29, 2012 - Feb 28, 2013
            Mar 1, 2013 - Feb 28, 2014
            Mar 1, 2014 - Feb 28, 2015

        Each result will contain a tuple of the sample photo, a start date, and an
        end date. Note the last end date is in the future.
        """
        start = self.first_photo.created_time.date()
        while True:
            photo = db.session.query(Photo).filter(
                Photo.created_time>=start
            ).order_by(Photo.created_time).first()

            if not photo:
                break

            if start.day != 1:
                first_day_of_month = date(start.year, (start.month + 1) % 12, 1)
            else:
                first_day_of_month = start

            end = first_day_of_month + relativedelta(years=1) - relativedelta(days=1)

            # Update what page we're on
            self.year = photo.created_time.date().year

            yield photo, start, end
            start = end + relativedelta(days=1)

    @property
    def page(self):
        return self.year or self.start

    @property
    def start(self):
        return self.first_photo.created_time.date().year


class MonthPaginator(Paginator):
    @property
    def end(self):
        last_date_in_year = date(self.year, 12, 31)

        end = min(self.last_photo.created_time.date(), last_date_in_year).month
        return end

    def iter_pages(self):
        """Yields a sample photo and date range from each month of that year and
        stops iteration when it reaches the latest photo in the database.

        It starts on a photo offset by the very first photo in the database.
        For example, if the first photo was in March 2012, and we are asking
        for months of 2013, it will return 12 months starting in March 2013 and
        not January 2013.
        """
        start = date(self.year, self.start, 1)
        while True:
            photo = db.session.query(Photo).filter(
                    Photo.created_time>=start
            ).order_by(Photo.created_time).first()

            if not photo:
                break

            end = start + relativedelta(months=1) - relativedelta(days=1)

            # Update what page we're on
            self.month = photo.created_time.date().month

            yield photo, start, end
            start = end + relativedelta(days=1)

    @property
    def page(self):
        return self.month or self.start

    @property
    def start(self):
        return self.first_photo.created_time.date().month


class DayPaginator(Paginator):
    @property
    def end(self):
        __, last_day = monthrange(self.year, self.month)
        last_date_in_month = date(self.year, self.month, last_day)

        end = min(self.last_photo.created_time.date(), last_date_in_month).day
        return end

    def iter_pages(self):
        """Yields a sample photo for each day of the month and stops iteration
        either when it reaches the end of the month or the latest photo in the
        database.
        """
        start = date(self.year, self.start, self.day)
        while True:
            end = start + relativedelta(days=1)

            photo = db.session.query(Photo).filter(
                    Photo.created_time>=start,
                    Photo.created_time<=end
            ).order_by(Photo.created_time).first()

            if not photo:
                break

            self.day = photo.created_time.date().day

            yield photo, start, end
            start = end

    @property
    def page(self):
        return self.day or self.start

    @property
    def start(self):
        return self.first_photo.created_time.date().day


class Pagination(object):
    def __init__(self, year, month=None, day=None):
        self.year = year
        self.month = month
        self.day = day
        self._paginator = self._identify_paginator()

    @property
    def has_prev(self):
        return self.page > self._paginator.start

    @property
    def has_next(self):
        return self.page < self._paginator.end

    def iter_pages(self):
        return self._paginator.iter_pages()

    @property
    def page(self):
        return self._paginator.page

    @property
    def pages(self):
        return self._paginator.end - self._paginator.start + 1

    def _identify_paginator(self):
        try:
            date(self.year, max(self.month, 1), max(self.day, 1))
        except:
            raise ValueError('Date does not exist!')

        if self.day and self.month and self.year:
            return DayPaginator(self.year, self.month, self.day)
        elif self.month and self.year:
            return MonthPaginator(self.year, self.month)
        elif self.year:
            return YearPaginator(self.year)
        else:
            raise ValueError('Unsupported pagination!')
