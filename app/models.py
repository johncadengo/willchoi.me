from . import db


locations_photos = db.Table('locations_photos',
    db.Column('location_id', db.Integer(), db.ForeignKey('locations.id')),
    db.Column('photo_id', db.Integer(), db.ForeignKey('photos.id')))

photos_tags = db.Table('photos_tags',
    db.Column('photo_id', db.Integer(), db.ForeignKey('photos.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tags.id')))


class Image(db.Model):
    __tablename__ = 'images'

    id = db.Column(db.Integer(), primary_key=True)
    height = db.Column(db.Float())
    width = db.Column(db.Float())
    url = db.Column(db.Text())
    type = db.Column(db.String(64)) # Thumbnail, Low Res, Standard Res

    photo_id = db.Column(db.ForeignKey('photos.id'))


class Location(db.Model):
    __tablename__ = 'locations'

    id = db.Column(db.Integer(), primary_key=True)
    instagram_id = db.Column(db.String(255), unique=True)
    latitude = db.Column(db.Float())
    longitude = db.Column(db.Float())
    name = db.Column(db.String(255))


class Photo(db.Model):
    __tablename__ = 'photos'

    id = db.Column(db.Integer(), primary_key=True)
    instagram_id = db.Column(db.String(255), unique=True)
    caption = db.Column(db.Text())
    created_time = db.Column(db.DateTime())
    featured_on = db.Column(db.String(255))
    link = db.Column(db.Text())

    images = db.relationship('Image',
        backref=db.backref('photo', lazy='joined', order_by='Image.width'))
    locations = db.relationship('Location', secondary=locations_photos,
        backref=db.backref('photos', lazy='dynamic'))
    tags = db.relationship('Tag', secondary=photos_tags,
        backref=db.backref('photos', lazy='dynamic'))

    # This assumes that the instagram api always returns 3 images
    @property
    def thumbnail_image(self):
        try:
            return self.images[0]
        except IndexError:
            return None

    @property
    def low_res_image(self):
        try:
            return self.images[1]
        except IndexError:
            return None

    @property
    def standard_res_image(self):
        try:
            return self.images[2]
        except IndexError:
            return None


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(255), unique=True)

    def __hash__(self):
        return hash(self.name)
