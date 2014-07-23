from datetime import datetime

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

        self.assertIn(image, db.session)

    def test_create_photo(self):
        # Start with photo
        photo = Photo()
        photo.instagram_id = '757677846642235453_1134805'
        photo.caption = '126. Who needs fireworks anyway'
        photo.created_time = datetime(2012, 02, 29)
        photo.featured_on = 'Josh Johnson; #JJ'
        photo.link = 'http://instagram.com/p/qDVDHkyxvS/'

        db.session.add(photo)
        db.session.commit()

        self.assertIn(photo, db.session)

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

        self.assertTrue(all(i in db.session for i in images))

        # Connect images to photo
        photo.images.extend(images)
        db.session.commit()

        self.assertTrue(all(i in photo.images for i in images))
        self.assertTrue(all(photo is i.photo for i in images))

        # Mock location and tag
        loc = Location()
        loc.instagram_id = '1'
        loc.name = 'Dogpatch Labs'
        loc.latitude = 37.782
        loc.longitude = -122.387

        db.session.add(loc)
        db.session.commit()

        self.assertIn(loc, db.session)

        tag = Tag()
        tag.name = 'july4th'

        db.session.add(tag)
        db.session.commit()

        self.assertIn(tag, db.session)

        # Connect location and tag to photo
        photo.locations.append(loc)
        photo.tags.append(tag)

        db.session.commit()

        self.assertIn(loc, photo.locations)
        self.assertIn(tag, photo.tags)
        self.assertIn(photo, loc.photos)
        self.assertIn(photo, tag.photos)
