from calendar import monthrange
from datetime import date
from dateutil.relativedelta import relativedelta

from . import db
from .models import Photo


class Paginator(object):
    def __init__(self, year=None, month=None, day=None):
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
        return self.last_photo.created_time.date()

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
        photo = self.first_photo
        start = self.start
        while photo:
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

    @property
    def page(self):
        return self.year or self.start

    @property
    def start(self):
        return self.first_photo.created_time.date()


class MonthPaginator(Paginator):
    @property
    def end(self):
        last_date_in_year = date(self.year, 12, 31)

        end = min(self.last_photo.created_time.date(), last_date_in_year).month
        return end

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

    @property
    def page(self):
        return self.day or self.start

    @property
    def start(self):
        return self.first_photo.created_time.date().day


class Pagination(object):
    def __init__(self, year=None, month=None, day=None):
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
        if self.month and self.year:
            return DayPaginator(self.year, self.month, self.day)
        elif self.year:
            return MonthPaginator(self.year, self.month)
        elif not self.month and not self.day:
            return YearPaginator(self.year)
        else:
            raise ValueError('Unsupported pagination!')
