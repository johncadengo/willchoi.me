from app import db
from app.models import Image, Location, Photo, Tag

from tests import TestCase


class TestImage(TestCase):

    def test_create_image(self):
        image = Image()
        image.height = 640
        image.width = 640
        image.url = 'http://scontent-b.cdninstagram.com/hphotos-xpa1/t51.2885-15/10522310_677385995673625_267718762_n.jpg'
        image.type = 'standard_resolution'

        db.session.add(image)
        db.session.commit()

        assert image in db.session
