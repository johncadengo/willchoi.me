from datetime import datetime

from app import db
from app.helpers import get_years
from app.models import Photo

from tests import TestCase


class TestGetYears(TestCase):

    def test_get_years(self):
        # Set up some mock objects
        first_photo = Photo()
        first_photo.created_time = datetime(2012, 02, 29)

        db.session.add(first_photo)
        db.session.commit()

        self.assertIn(first_photo, db.session)

        # Year two
        second_photo = Photo()
        second_photo.created_time = datetime(2013, 01, 01)

        db.session.add(second_photo)
        db.session.commit()

        self.assertIn(second_photo, db.session)

        # Year three
        third_photo = Photo()
        third_photo.created_time = datetime(2014, 01, 01)

        db.session.add(third_photo)
        db.session.commit()

        self.assertIn(third_photo, db.session)

        # We should get 3 photos back with the expected date range
        expected_years = [
            (None, datetime(2012, 02, 29), datetime(2013, 02, 28)),
            (None, datetime(2013, 03, 01), datetime(2014, 02, 28)),
            (None, datetime(2014, 03, 01), datetime(2015, 02, 28))
        ]
        for expected, actual in zip(expected_years, get_years()):
            self.assertEqual(expected, actual)
