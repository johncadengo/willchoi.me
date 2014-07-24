from datetime import date
from dateutil.relativedelta import relativedelta
from itertools import izip

from app import db
from app.helpers import Pagination
from app.models import Photo

from tests import TestCase


class TestHelpers(TestCase):

    def test_day_paginator_two_dates(self):
        # Start
        first_photo = Photo()
        first_photo.created_time = date(2013, 03, 01)

        db.session.add(first_photo)
        db.session.commit()

        self.assertIn(first_photo, db.session)

        # End
        second_photo = Photo()
        second_photo.created_time = date(2013, 03, 15)

        db.session.add(second_photo)
        db.session.commit()

        self.assertIn(second_photo, db.session)

        # Create day pagination
        pagination = Pagination(2013, 03, 01)

        self.assertEqual(1, pagination.page)
        self.assertEqual(15, pagination.pages)
        self.assertFalse(pagination.has_prev)
        self.assertTrue(pagination.has_next)

        # Create month pagination
        pagination = Pagination(2013, 03)

        self.assertEqual(3, pagination.page)
        self.assertEqual(1, pagination.pages)
        self.assertFalse(pagination.has_prev)
        self.assertFalse(pagination.has_next)

        # Create year pagination
        pagination = Pagination(2013)

        self.assertEqual(2013, pagination.page)
        self.assertEqual(1, pagination.pages)
        self.assertFalse(pagination.has_prev)
        self.assertFalse(pagination.has_next)

        # Widen range
        second_photo.created_time = date(2013, 03, 31)
        db.session.commit()

        pagination = Pagination(2013, 03, 01)

        self.assertEqual(1, pagination.page)
        self.assertEqual(31, pagination.pages)
        self.assertFalse(pagination.has_prev)
        self.assertTrue(pagination.has_next)

    def test_day_paginator_iter(self):
        # Start
        photos = [Photo(created_time=(date(2012, 01, day + 1))) for day in xrange(31)]

        db.session.add_all(photos)
        db.session.commit()

        for photo in photos:
            self.assertIn(photo, db.session)

        pagination = Pagination(2012, 01, 01)

        self.assertEqual(1, pagination.page)
        self.assertEqual(31, pagination.pages)

        # Check these before and after iterating through paginator
        self.assertFalse(pagination.has_prev)
        self.assertTrue(pagination.has_next)

        expected_days = [(photos[day], date(2012, 01, day + 1),
                         date(2012, 01, day + 1) + relativedelta(days=1))
                         for day in xrange(31)]
        for expected, actual in izip(expected_days, pagination.iter_pages()):
            self.assertEqual(expected, actual)
            self.assertEqual(expected[1].day, pagination.page)

        self.assertTrue(pagination.has_prev)
        self.assertFalse(pagination.has_next)

    def test_one_year_paginator(self):
        photo = Photo()
        photo.created_time = date(2012, 02, 29)

        db.session.add(photo)
        db.session.commit()

        self.assertIn(photo, db.session)

        # This should only run once since the db only has 1 year initially
        pagination = Pagination(2012)
        self.assertEqual(1, len(list(pagination.iter_pages())))

    def test_year_paginator(self):
        # Set up some mock objects
        first_photo = Photo()
        first_photo.created_time = date(2012, 02, 29)

        db.session.add(first_photo)
        db.session.commit()

        self.assertIn(first_photo, db.session)

        # Year two
        second_photo = Photo()
        second_photo.created_time = date(2013, 03, 01)

        db.session.add(second_photo)
        db.session.commit()

        self.assertIn(second_photo, db.session)

        # Year three
        third_photo = Photo()
        third_photo.created_time = date(2014, 03, 01)

        db.session.add(third_photo)
        db.session.commit()

        self.assertIn(third_photo, db.session)

        # Create pagination after photos
        pagination = Pagination(2012)

        self.assertEqual(3, pagination.pages)

        # Check these before and after iterating through paginator
        self.assertFalse(pagination.has_prev)
        self.assertTrue(pagination.has_next)

        # We should get 3 photos back with the expected date range
        expected_years = [
            (first_photo, date(2012, 02, 29), date(2013, 02, 28)),
            (second_photo, date(2013, 03, 01), date(2014, 02, 28)),
            (third_photo, date(2014, 03, 01), date(2015, 02, 28))
        ]
        for expected, actual in izip(expected_years, pagination.iter_pages()):
            self.assertEqual(expected, actual)
            self.assertEqual(expected[1].year, pagination.page)

        self.assertTrue(pagination.has_prev)
        self.assertFalse(pagination.has_next)
