from datetime import date

from app import db
from app.helpers import get_years
from app.models import Photo

from tests import TestCase


class TestHelpers(TestCase):

    def test_get_years_one_year(self):
        # This should only run once since the db only has 1 year initially
        self.assertEqual(1, len(list(get_years())))

    def test_get_years(self):
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

        # We should get 3 photos back with the expected date range
        expected_years = [
            (first_photo, date(2012, 02, 29), date(2013, 02, 28)),
            (second_photo, date(2013, 03, 01), date(2014, 02, 28)),
            (third_photo, date(2014, 03, 01), date(2015, 02, 28))
        ]
        for expected, actual in zip(expected_years, get_years()):
            self.assertEqual(expected, actual)
