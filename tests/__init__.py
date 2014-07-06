from datetime import datetime

from flask import Flask
from flask.ext.testing import TestCase as Base

from app import create_app, db
from app.models import Image, Location, Photo, Tag


class TestCase(Base):

    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True

    def create_app(self):
        # Pass in test configurations
        return create_app(self)

    def setUp(self):
        db.create_all()

        # Mock objects

        # Start with photo
        photo = Photo()
        photo.instagram_id = '757677846642235453_1134805'
        photo.caption = '126. Who needs fireworks anyway'
        photo.created_time = datetime.fromtimestamp(1404542259)
        photo.featured_on = 'Josh Johnson; #JJ'
        photo.link = 'http://instagram.com/p/qDVDHkyxvS/'

        db.session.add(photo)
        db.session.commit()

        assert photo in db.session

        # Mock some images
        hi_img = Image()
        hi_img.height = 640
        hi_img.width = 640
        hi_img.url = 'http://scontent-b.cdninstagram.com/hphotos-xpa1/t51.2885-15/10522310_677385995673625_267718762_n.jpg'
        hi_img.type = 'standard_resolution'

        low_img = Image()
        low_img.height = 306
        low_img.width = 306
        low_img.url = 'http://scontent-b.cdninstagram.com/hphotos-xpa1/t51.2885-15/10522310_677385995673625_267718762_a.jpg'
        low_img.type = 'low_resolution'

        thumb_img = Image()
        thumb_img.height = 150
        thumb_img.width = 150
        thumb_img.url = 'http://scontent-b.cdninstagram.com/hphotos-xpa1/t51.2885-15/10522310_677385995673625_267718762_s.jpg'
        thumb_img.type = 'thumbnail'

        images = [hi_img, low_img, thumb_img]
        db.session.add_all(images)
        db.session.commit()

        assert all(i in db.session for i in images)

        # Connect images to photo
        photo.images.extend(images)
        db.session.commit()

        assert all(i in photo.images for i in images)
        assert all(photo is i.photo for i in images)

        # Mock location and tag
        loc = Location()
        loc.instagram_id = '1'
        loc.name = 'Dogpatch Labs'
        loc.latitude = 37.782
        loc.longitude = -122.387

        db.session.add(loc)
        db.session.commit()

        assert loc in db.session

        tag = Tag()
        tag.name = 'july4th'

        db.session.add(tag)
        db.session.commit()

        assert tag in db.session

        # Connect location and tag to photo
        photo.locations.append(loc)
        photo.tags.append(tag)

        db.session.commit()

        assert loc in photo.locations
        assert tag in photo.tags
        assert photo in loc.photos
        assert photo in tag.photos

    def tearDown(self):
        db.session.remove()
        db.drop_all()
